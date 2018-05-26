from flask_restful import Resource, reqparse
from flask import render_template

from web_queue import api, app, db
from web_queue.queue import TaskQueue
from config import Config


@app.route('/')
def index():
    tq = TaskQueue(Config.SQLALCHEMY_DATABASE_URI)
    tq.get_all()
    return render_template('index.html', task_queue=tq)


class TaskAPI(Resource):
    def __init__(self):
        self.task_queue = TaskQueue()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True, location='json')
        self.reqparse.add_argument('params', type=str, required=True, location='json')
        super(TaskAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        task = {
            'name': args['name'],
            'params': args['params']
        }
        self.task_queue.append()


api.add_resource(TaskAPI, '/task-runner/api/', endpoint='task')
