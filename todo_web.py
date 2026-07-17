from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
STORAGE_FILE = 'tasks.json'

def load_tasks():
    """Load tasks from JSON file."""
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_tasks(tasks):
    """Save tasks to JSON file."""
    with open(STORAGE_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

@app.route('/')
def index():
    """Serve the to-do list page."""
    return render_template('todo.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks."""
    return jsonify(load_tasks())

@app.route('/api/tasks', methods=['POST'])
def add_task():
    """Add a new task."""
    data = request.json
    tasks = load_tasks()
    
    task = {
        'id': len(tasks) + 1,
        'title': data.get('title'),
        'priority': data.get('priority', 'medium'),
        'completed': False,
        'created_at': datetime.now().isoformat(),
        'due_date': data.get('due_date')
    }
    
    tasks.append(task)
    save_tasks(tasks)
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update task status."""
    data = request.json
    tasks = load_tasks()
    
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = data.get('completed', task['completed'])
            task['title'] = data.get('title', task['title'])
            task['priority'] = data.get('priority', task['priority'])
            save_tasks(tasks)
            return jsonify(task)
    
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    tasks = load_tasks()
    tasks = [t for t in tasks if t['id'] != task_id]
    save_tasks(tasks)
    return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
