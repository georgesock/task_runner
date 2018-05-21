from flask_restful import Resource, reqparse

from app import app, db, api
from app.queue import TaskQueue


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
