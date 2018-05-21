from multiprocessing import Pool
import types

from config import Config
# from app import task_runner


class BaseTask(object):
    def __init__(self, name, params):
        self._name = name
        self.params = params
        self._func = None

    def run(self):
        pass

    @property
    def func(self):
        return self._func

    @func.setter
    def func(self, f):
        self._func = f
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def __repr__(self):
        return 'Task %s' % self.name


# class Consumer(object):
#     def __init__(self):
#         self.pool = Pool(Config.WORKERS)
#         self.tasks_path = Config.TASKS_PATH
#         self.app = task_runner
#
#     @staticmethod
#     def get_function(name):
#         task = task_runner.tasks.get(name)
#         return task.run
#
#     def save_results_to_db(self):
#         print 'task ends'
#
#     def apply_async(self, name):
#         func = self.get_function(name)
#         task_result = self.pool.apply_async(func, callback=self.save_results_to_db)


class Producer(object):
    def __init__(self):
        self.tasks = {}


class TaskRunner(object):
    def __init__(self):
        self._tasks = {}

    def register_task_type(self, name, task):
        self._tasks[name] = task

    @property
    def tasks(self):
        return self._tasks

    def task(self, name, params=None):
        def func_wrapper(func):
            task = BaseTask(name, params)
            task.run = types.MethodType(func, task)
            self._tasks[name] = task
            return task
        return func_wrapper