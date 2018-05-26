from app.task_runner import TaskRunner, BaseTask
from config import Config

print Config.SQLALCHEMY_DATABASE_URI
app = TaskRunner(Config.SQLALCHEMY_DATABASE_URI)


@app.task(name='test1')
def long_long(params=None):
    for i in xrange(2):
        print 2**i
    return 'Hello'


@app.task(name='test2')
def long_long2(params=None):
    for i in xrange(100):
        print 2**i


class LoopTask(BaseTask):
    def __init__(self, name, params):
        BaseTask.__init__(self, name, params)

    def run(self):
        while True:
            pass

# if __name__ == '__main__':
    # print app._tasks
    # print app._tasks['test1'].run
    # print app._tasks['test1'].run()

    # print tasks.producer.tasks
    # t = tasks.long_long()
    # print t.name

    # print tasks.producer.modules
    # print dir(t)
    # print t.run()

    # t2 = LoopTask('loop', None)
    # app.register_task_type('loop', t2)
    # print app._tasks['loop'].run




