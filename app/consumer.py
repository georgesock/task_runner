from multiprocessing import Process
import types
import time
import logging
import signal

from config import Config
from app import task_runner
from app.exceptions import QueueException



class Worker(object):
    def __init__(self, app, default_delay, max_delay, backoff, utc):
        self._logger = logging.getLogger('TaskRunner.consumer.Worker')
        self.app = app
        self.delay = default_delay
        self.max_delay = max_delay

    def popleft(self):
        try:
            task = self.app.queue.popleft()
        except QueueException:
            self._logger.info('Can not write to Queue')
        else:
            self._logger.info('Pop task', task)
        return task

    def loop(self):
        task = None
        exception_raised = True
        try:
            task = self.app.queue.popleft()
        except QueueException:
            self._logger.info('Queue Exception')
        except KeyboardInterrupt:
            raise
        except:
            self._logger.info('Error')
        else:
            exception_raised = False

        if task:
            self.process_task(task)
        elif exception_raised:
            self.sleep()

    def sleep(self):
        if self.delay > self.max_delay:
            self.delay = self.max_delay
        self._logger.info("No message, sleeping %s", self.delay)
        time.sleep(self.delay)

    def process_task(self, task):
        self._logger.info('Execution %s', task)
        exception = None
        task_value = None

        try:
            if not isinstance(task, task_runner.BaseTask):
                raise TypeError('Unknow object')
            task_value = task.run()
        except Exception:
            self._logger.info("Some Error")




class Consumer(object):
    def __init__(self):
        self.workers = Config.WORKERS
        self.workers_threads = []
        self.consumer_timeout = 0.1
        self.tasks_path = Config.TASKS_PATH
        self.app = task_runner
        self._logger = logging.getLogger('TaskRunner.consumer')


    def start(self):
        self._logger.info('Starting Consumer')
        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        if hasattr(signal, 'SIGHUP'):
            original_sighup_handler = signal.signal(signal.SIGHUP, signal.SIG_IGN)

        for _, worker_process in self.worker_threads:
            worker_process.start()

        signal.signal(signal.SIGINT, original_sigint_handler)
        if hasattr(signal, 'SIGHUP'):
            signal.signal(signal.SIGHUP, original_sighup_handler)

    def stop(self, graceful=False):
        if graceful:
            self._logger.info('Shutting down gracefully...')
            try:
                for _, worker_process in self.workers_treads:
                    worker_process.join()
            except KeyboardInterrupt:
                self._logger.info('Request for shutting down...')
            else:
                self._logger.info('All workers have stopped')
        else:
            self._logger.info('Shutting down...')

    def run(self):
        self.start()
        timeout = self.consumer_timeout
        while True:
            try:
                time.sleep(timeout)
            except KeyboardInterrupt:
                self.stop()
            except:
                self._logger.info('Error in Consumer')
                self.stop()

    @staticmethod
    def get_function(name):
        task = task_runner.tasks.get(name)
        return task.run

    def save_results_to_db(self):
        print 'task ends'

    def apply_async(self, name):
        func = self.get_function(name)
        task_result = self.pool.apply_async(func, callback=self.save_results_to_db)

if __name__ == '__main__':
    consumer = Consumer()
    consumer.run()
