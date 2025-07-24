from datetime import date
from sqlalchemy import desc
from flask import Blueprint, request, jsonify
from backend.app.models.tasks import tasks, engine

tasks_bp = Blueprint('tasks', __name__)

def build_task_response(task):
    return {
        'id': task['id'],
        'title': task['title'],
        'description': task['description'] if task['description'] else None,
        'priority': task['priority'],
        'completed': task['completed'],
        'date': task['date'].isoformat() if task['date'] else None
    }

@tasks_bp.route('/tasks', methods=['POST'])
def add_task():
    # Get json
    data = request.json

    # Return error if no JSON data received
    if data is None:
        return jsonify({'error': 'No JSON data received'}), 400

    # Return error if not all required field are received
    required_fields = ['title', 'completed', 'priority']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    # Return error if priority is not a number 0-5
    try:
        task_priority = int(data['priority'])
        if task_priority < 0 or task_priority > 5:
            return jsonify({'error': 'Priority must be between 0 and 5'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Priority should be a number'}), 400

    # Return error if completed is not a boolean
    if data['completed'] not in [True, False]:
        return jsonify({'error': 'Completed should be a boolean'}), 400

    # Add to the database
    try:
        with engine.begin() as conn:
            insert_statement = tasks.insert().values(
            title = data['title'],
            priority = task_priority,
            completed = data['completed'],
            description = data.get('description', ''),
            date = date.today()
            )
            conn.execute(insert_statement)
    except Exception as e:
        return jsonify({'error': f'Error adding task: {str(e)}'}), 500
    
    # Return success message
    return jsonify({'message': 'Task succesfully added'}), 201

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    # Get all tasks
    try:
        with engine.begin() as conn:
            select_statement = tasks.select().order_by(desc(tasks.c.date), desc(tasks.c.id))
            result = conn.execute(select_statement).fetchall()
    except Exception as e:
        return jsonify({'error': f'Error getting tasks: {str(e)}'}), 500

    # Return empty list if no task was found
    if not result:
        return jsonify([]), 200

    # Convert every task to dict format
    tasks_list = [build_task_response(task) for task in result]

    # Return transactions in JSON format
    return jsonify(tasks_list), 200

@tasks_bp.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    # Get task
    try:
        with engine.begin() as conn:
            select_statement = tasks.select().where(tasks.c.id == id)
            result = conn.execute(select_statement).fetchone()
    except Exception as e:
        return jsonify({'error': f'Error getting task: {str(e)}'}), 500

    # Return error if task not fount
    if not result:
        return jsonify({'error': 'Task not found'}), 404
    
    # Convert task to dictionary
    task_dict = build_task_response(result)

    return jsonify(task_dict), 200
