from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from config import Config
from app import BaseTask
from app.task_runner import TaskRunner


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
api = Api(app)

task_runner = TaskRunner()

#from app import routes, models, errors
from app import routes
