# Task Runner App
## System Requirements:
1. Linux OS (windows doesn't support multiprocessing)
2. PostgreSQL 9
3. Python 2
4. pip

## Installation instractions
1. git clone project, than cd to the project root directory
2. Create virtual environment for python:

    ```bash
    python -m venv .env
    ```
3. Install python dependencies:

    ```bash
    .env/bin/pip install -r requirements.txt
    ```
4. Create database **task_runner** in postgreSQL server:
    ```sql
    -- DROP DATABASE task_runner;

    CREATE DATABASE task_runner
      WITH OWNER = postgres
           ENCODING = 'UTF8'
           TABLESPACE = pg_default
           LC_COLLATE = 'en_US.UTF-8'
           LC_CTYPE = 'en_US.UTF-8'
           CONNECTION LIMIT = -1;
    ```
## Starting web_queue application:
1. cd to project root directory
2. Start up web_queue flask application:

    ```bash
    .env/bin/python start_web_queue.py
    ```
3. Go to [web_queue app localhost:5000](http://localhost:5000/)
## Starting consumer application:
1. cd to project root directory
2. Start up consumer application in console:

    ```bash
    .env/bin/python start_consumer.py
    ```
## Creating app with tasks 
1. The example of app locates in tasks.py in project root directory:

    ```python
    import time

    from app.task_runner import TaskRunner, BaseTask
    from config import Config

    app = TaskRunner(Config.SQLALCHEMY_DATABASE_URI)


    @app.task(name='m_sleep')
    def middle_sleep(self=None):
        print 'Middle sleep 30s'
        time.sleep(30)
        return 'Hello1'


    @app.task(name='l_sleep')
    def long_sleep(self=None):
        print 'Long sleep 60s'
        time.sleep(60)
        return 'Hello2'

    @app.task(name='inf_loop')
    def infinete_loop(self=None):
        while True:
            pass
         
    if __name__ == '__main__':
       app.tasks['l_sleep'].delay()

    ```
2. Run script with application:
    ```bash
    .env/bin/python tasks.py
    ```
3. The task will appeared in web_queue page. 
than worker will take it to process. 




