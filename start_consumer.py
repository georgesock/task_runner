import os
import sys
import argparse

from app.task_runner import TaskRunner
from app.consumer import Consumer


def load_app(app_path):
    __import__(app_path)
    mod = sys.modules[app_path]
    from pprint import pprint
    pprint(mod)
    for o in mod.__dict__:
        if isinstance(mod.__dict__[o], TaskRunner):
            return mod.__dict__[o]
    else:
        raise ImportError()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start Consumer')
    parser.add_argument('-A', '-app', help='TaskRunner Application path', default='tasks')
    app_path = parser.parse_args()
    app = load_app(app_path.A)
    consumer = Consumer(app, 2)
    consumer.run()


