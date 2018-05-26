import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or "#$@#$safasdfsa23432"
    POSTGRES_SERVER = '127.0.0.1:5432'
    POSTGRES_USER = 'postgres'
    POSTGRES_PASS = ''
    POSTGRES_DB = 'task_runner'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URI')
                                or 'postgres+psycopg2://{user}:{pw}@{db_server}/{db}'.format(user=POSTGRES_USER,
                                                                                     pw=POSTGRES_PASS,
                                                                                     db_server=POSTGRES_SERVER,
                                                                                     db=POSTGRES_DB))
    print(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENCODE_BASE = "23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"
    TASKS_PATH = ['tasks.py']
    WORKERS = 2
