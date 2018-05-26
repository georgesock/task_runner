import types
from web_queue.models import DB
from web_queue.queue import TaskQueue


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


class Producer(object):
    def __init__(self):
        self.tasks = {}


class TaskRunner(object):
    def __init__(self, db_uri):
        self._tasks = {}
        self.db = DB(db_uri)
        self.tasks_queue = TaskQueue()

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



