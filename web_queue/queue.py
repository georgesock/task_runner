from web_queue.models import Queue, DB


class TaskQueue(object):
    def __init__(self, db_uri):
        self.db = DB(db_uri)
        self.session = self.db.get_session()

    def __len__(self):
        return Queue.count()

    def __iter__(self):
        tasks = self.get_all()
        for task in tasks:
            yield task

    def count(self):
        return (self.session.query(Queue)).count()

    def get_all(self):
        query = self.session.query(Queue)
        all = query.all()
        return list(all)

    def append(self, name, params):
        q = Queue(name=name, params=params)

        self.session.add(q)
        self.session.commit()

    def pop(self):
        task = self.session.query.order_by(Queue.id).first()
        self.session.delete(task)
        self.session.commit()
        return task


if __name__ == '__main__':
    from config import Config
    tq = TaskQueue(Config.SQLALCHEMY_DATABASE_URI)
    r = tq.get_all()
    print r


