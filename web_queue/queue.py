import logging

from web_queue.models import Queue, DB


class TaskQueue(object):
    def __init__(self, db_uri):
        self.db = DB(db_uri)
        self.session = self.db.get_session()
        self._logger = logging.getLogger('TaskQueue Instance')

    def __len__(self):
        return Queue.count()

    def __iter__(self):
        tasks = self.get_all()
        for task in tasks:
            yield task

    def count(self):
        return (self.session.query(Queue)).count()

    def get_all(self):
        all_tasks = self.session.query(Queue).all()
        return all_tasks

    def append(self, name, params):
        q = Queue(name=name, params=params)
        self.session.add(q)
        self.session.commit()

    def pop(self):
        task = self.session.query(Queue).order_by(Queue.id).first()
        if task:
            self.session.delete(task)
            self.session.commit()
            return task

    def peek(self, worker_id):
        task = self.session.query(Queue).filter(Queue.worker == None).order_by(Queue.id).with_for_update().first()
        if task:
            self._logger.info("Get free task %s", task)
            task.worker = worker_id
            try:
                self._logger.info("Mark for worker %s", worker_id)
                self.session.add(task)
                self.session.commit()
            except:
                self.session.rollback()
            return task

    def delete(self, id):
        task = self.session.query(Queue).get(id)
        self.session.delete(task)
        self.session.flush()
        self.session.commit()

    def delete_all(self):
        task = self.session.query(Queue).delete()
        self.session.flush()
        self.session.commit()


if __name__ == '__main__':
    from config import Config
    tq = TaskQueue(Config.SQLALCHEMY_DATABASE_URI)
    r = tq.get_all()
    print r


