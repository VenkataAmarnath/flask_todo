from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class TodoAPI:
    def __init__(self):
        self.users_file = "users.json"
        self.data_file = "data.json"
        
    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                return json.load(file)
        return {"users": []}

    def load_tasks(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                return json.load(file)
        return {}

    def save_users(self, users_data):
        with open(self.users_file, 'w') as file:
            json.dump(users_data, file)

    def save_tasks(self, tasks_data):
        with open(self.data_file, 'w') as file:
            json.dump(tasks_data, file)

api = TodoAPI()

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(api.load_users())

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    users_data = api.load_users()
    if data['username'] not in users_data['users']:
        users_data['users'].append(data['username'])
        api.save_users(users_data)
        return jsonify({"message": "User added successfully"})
    return jsonify({"error": "User already exists"}), 400

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(api.load_tasks())

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    tasks_data = api.load_tasks()
    
    if data['user'] not in tasks_data:
        tasks_data[data['user']] = {}
    
    tasks_data[data['user']][data['task']] = data['status']
    api.save_tasks(tasks_data)
    return jsonify({"message": "Task added successfully"})

@app.route('/api/tasks/status', methods=['PUT'])
def update_task_status():
    data = request.get_json()
    tasks_data = api.load_tasks()
    
    if data['user'] in tasks_data and data['task'] in tasks_data[data['user']]:
        tasks_data[data['user']][data['task']] = data['status']
        api.save_tasks(tasks_data)
        return jsonify({"message": "Status updated successfully"})
    return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)