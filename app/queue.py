from app.models import Queue
from app import db


class TaskQueue(object):

    def __len__(self):
        return Queue.count()

    def __iter__(self):
        tasks = Queue.iterate()
        for task in tasks:
            yield task

    def append(self, name, params):
        Queue.append(name, params)

    def popleft(self):
        task = Queue.popleft()
        return task


if __name__ == '__main__':
    tq = TaskQueue()
    tq.append('sfasf', 'sdfsaf')
    for t in tq:
        print t
