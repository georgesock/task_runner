from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

from web_queue.utils import singleton

Base = declarative_base()


class Queue(Base):
    __tablename__ = 'queue'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), index=True)
    params = Column(String(1000))

    def __repr__(self):
        return 'Task %s' % (self.name)


@singleton
class DB(object):

    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)

    def get_session(self):
        Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return Session()

