import logging
import signal
import time
from multiprocessing import Event as ProcessEvent
from multiprocessing import Process

from app_exceptions import QueueException
from app import task_runner

logging.basicConfig(level=logging.INFO)


class Worker(object):
    def __init__(self, task_runner, delay):
        self._logger = logging.getLogger('Consumer.Worker')
        self.delay = delay
        self.task_runner = task_runner

    def loop(self):
        task = None
        exception = True
        try:
            task = self.task_runner.task_queue.pop()
            self._logger.info('Try to get task')
        except QueueException:
            self._logger.info('Queue pop raised exception')
        except KeyboardInterrupt:
            raise
        except:
            self._logger.info('Unknown Error')
        else:
            exception = False
        if task:
            self.process_task(task)
        elif exception:
            self._logger.info('No messages in Task Queue')
            time.sleep(self.delay)

    def process_task(self, task):
        try:
            task_result = self.task_runer.execute(task)
        except KeyboardInterrupt:
            self._logger.info('Receiving exit signal')
        except:
            self._logger.info('Unhandled exception in working thread')


class ProcessEnvironment(object):
    def get_stop_flag(self):
        return ProcessEvent()

    def create_process(self, runnable, name):
        p = Process(target=runnable, name=name)
        p.daemon = True
        return p

    def is_alive(self, proc):
        return proc.is_alive()


class Consumer(object):
    def __init__(self, task_runner, workers=1):
        self.consumer_timeout = 0.1
        self.max_delay = 10.0
        self._logger = logging.getLogger('Consumer')
        self._logger.setLevel(logging.INFO)
        self.environment = ProcessEnvironment()
        self.task_runner = task_runner
        self.workers_process = []
        for i in range(workers):
            worker = self._create_worker()
            process = self._create_process(worker, 'Worker-%d' % (i+1))
            self.workers_process.append((worker, process))

    def _create_worker(self):
        return Worker(self.task_runner, self.max_delay)

    def _create_process(self, process, name):
        def _run():
            try:
                process.loop()
            except KeyboardInterrupt:
                pass
            except:
                self._logger.exception('Process %s died', name)
        return self.environment.create_process(_run, name)

    def start(self):
        self._logger.info('Starting Consumer')
        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        if hasattr(signal, 'SIGHUP'):
            original_sighup_handler = signal.signal(signal.SIGHUP, signal.SIG_IGN)

        for _, worker in self.workers_process:
            worker.start()

        signal.signal(signal.SIGINT, original_sigint_handler)
        if hasattr(signal, 'SIGHUP'):
            signal.signal(signal.SIGHUP, original_sighup_handler)

    def stop(self, graceful=False):
        if graceful:
            self._logger.info('Shutting down gracefully...')
            try:
                for _, worker in self.workers_process:
                    worker.join()
            except KeyboardInterrupt:
                self._logger.info('Request for shutting down...')
            else:
                self._logger.info('All workers have stopped')
        else:
            self._logger.info('Shutting down...')

    def run(self):
        self.start()
        timeout = self.consumer_timeout
        self._logger.info("Consumer started")
        while True:
            try:
                time.sleep(timeout)
                self._logger.info("Loop started")
            except KeyboardInterrupt:
                self._logger.info("Keyboard Iterrupt")
                self.stop()
            except:
                self._logger.info('Error in Consumer')
                self.stop()



if __name__ == '__main__':

    c = Consumer(task_runner)
    c.run()
