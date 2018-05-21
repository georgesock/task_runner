from app import db


class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), index=True)
    params = db.Column(db.String(1000))

    @classmethod
    def count(cls):
        return cls.query.count()

    @classmethod
    def iterate(cls):
        return cls.query.all()

    @classmethod
    def append(cls, task_name, params):
        q = Queue(task_name=task_name, params=params)
        db.session.add(q)
        db.session.commit()

    @classmethod
    def pop(cls):
        cls.query.order_by(cls.id).first()

    def __repr__(self):
        return '<Task %s: %s>' %(self.id, self.task_name)

