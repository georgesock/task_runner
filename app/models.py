from app import db


class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    params = db.Column(db.String(1000))

    @classmethod
    def count(cls):
        return cls.query.count()

    @classmethod
    def iterate(cls):
        return cls.query.all()

    @classmethod
    def append(cls, name, params):
        q = Queue(task_name=name, params=params)
        db.session.add(q)
        db.session.commit()

    @classmethod
    def popleft(cls):
        task = cls.query.order_by(cls.id).first()
        db.session.delete(task)
        db.session.commit()
        return task

    def __repr__(self):
        return '<Task %s: %s>' %(self.id, self.task_name)

