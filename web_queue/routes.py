import json
from flask_restful import Resource, reqparse
from flask import render_template, Response, request, abort, jsonify
from jsonschema import validate

from web_queue import api, app
from web_queue.queue import TaskQueue
from web_queue.utils import json_validation, to_json
from config import Config


@app.route('/')
def index():
    task_queue = TaskQueue(Config.SQLALCHEMY_DATABASE_URI)
    tasks = task_queue.get_all()
    return render_template('index.html', task_queue=tasks)


@app.route('/api/v1/tasks', methods=['GET'])
def get_tasks():
    task_queue = TaskQueue(Config.SQLALCHEMY_DATABASE_URI)
    tasks = task_queue.get_all()
    tasks_names = list([(task.name, task.worker) for task in tasks])
    json_response = jsonify({"tasks": tasks_names})
    return json_response

@app.route('/api/v1/tasks', methods=['DELETE'])
def delete_tasks():
    task_queue = TaskQueue(Config.SQLALCHEMY_DATABASE_URI)
    tasks = task_queue.delete_all()
    json_response = jsonify({"status": 'OK'})
    return json_response


@app.route('/api/v1/task', methods=['POST'])
def post_task():
    print request.json
    if not request.json:
        abort(404)
    task_queue = TaskQueue(Config.SQLALCHEMY_DATABASE_URI)
    task_name = request.json['name']
    task_params = request.json['params']
    task_queue.append(name=task_name, params=task_params)
    json_response = jsonify({"status": "OK"})
    return json_response


@app.errorhandler(400)
def page_not_found(e):
    return jsonify(400, {})


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(400, {})


@app.errorhandler(405)
def page_not_found(e):
    return jsonify(405, {})



# class TaskAPI(Resource):
#     def __init__(self):
#         self.task_queue = TaskQueue(Config.SQLALCHEMY_DATABASE_URI)
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('name', type=str, required=True, location='json')
#         self.reqparse.add_argument('params', type=str, required=True, location='json')
#         super(TaskAPI, self).__init__()
#
#     def post(self):
#         args = self.reqparse.parse_args()
#         task = {
#             'name': args['name'],
#             'params': args['params']
#         }
#         self.task_queue.append()
#
#
# api.add_resource(TaskAPI, '/task-runner/api/', endpoint='task')
