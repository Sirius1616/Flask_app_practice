#!/usr/bin/python3
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

app =  Flask(__name__)
auth = HTTPBasicAuth()

@app.route('/')
def hello():
    return 'Hello people'

tasks = [
    {
        'id': 1,
        'tittle': u'buy groceries',
        'description': u'Milk, Cheese, Butter, Fruit',
        'done': False
    },
    {
        'id': 2,
        'tittle': u'Learn python',
        'description': u'Need to get good python tutorial on the web',
        'done': True
    }
]



@app.route('/todo/api/v2.0/tasks/<int:task_id>', methods=['GET'])
def get_a_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task':task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def add_task():
    if not request.json or not request.json['tittle']:
        abort(400)
    task = {
        'id':tasks[-1]['id'] + 1,
        'tittle': request.json['tittle'],
        'description': request.json.get('description', '')

    }

    tasks.append(task)

    return jsonify({'tasks': tasks}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(tasks) == 0:
        return abort(404)
    if not request.json:
        return abort(400)
    if 'tittle' in request.json and type(request.json['tittle']) != str:
        return abort(400)
    if 'description' in request.json and type(request.json['description']) != str:
        return abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        return abort(400)
    task[0]['tittle'] = request.json.get('tittle', task[0]['tittle'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])

    return jsonify({'tasks': tasks[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>')
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        return abort(404)
    tasks.remove(task[0])
    return jsonify({'result':True})


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_task():
    return jsonify({'tasks':[make_public_task(item) for item in tasks]})

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorise():
    return jsonify({'error':'unauthorized access'}, 401)

if __name__ == '__main__':
    app.run(debug=True)

