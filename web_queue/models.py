from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Queue(Base):
    __tablename__ = 'queue'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), index=True)
    params = Column(String(1000))

    def __repr__(self):
        return '<Task %s: %s>' % (self.id, self.name)


class DB(object):
    __instance = None

    @staticmethod
    def get_instance():
        if not DB.__instance:
            DB()
        return DB.__instance

    def __init__(self, db_uri):
        if DB.__instance:
            raise Exception('DB has been already created')
        else:
            DB.__instance = self

        self.engine = create_engine(db_uri)

    def get_session(self):
        Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return Session()

