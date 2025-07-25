from flask import Blueprint, request, jsonify
from backend.app.validators.task_validator import validate_task, validate_task_update
from backend.app.services.task_service import create_task, get_tasks, get_task, delete_task, update_task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['POST'])
def add_task():
    data = request.json

    if data is None:
        return jsonify({'error': 'No JSON data received'}), 400

    if not validate_task(data):
        return jsonify({'error': 'Invalid task'}), 400

    try:
        task = create_task(data)
    except Exception as e:
        return jsonify({'error': f'Error adding task: {str(e)}'}), 500
    
    return jsonify(task), 201

@tasks_bp.route('/tasks', methods=['GET'])
def get_all_tasks():
    tasks = get_tasks()

    if not tasks:
        return jsonify([]), 200

    return jsonify(tasks), 200

@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_single_task(task_id):
    task = get_task(task_id)

    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(task), 200
    
@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_single_task(task_id):
    deleted_task = delete_task(task_id)

    if not deleted_task:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify(deleted_task), 200

@tasks_bp.route('/tasks/<int:task_id>', methods=['PATCH'])
def modify_task(task_id):
    data = request.json

    if data is None:
        return jsonify({'error': 'No JSON data received'}), 400

    task = get_task(task_id)

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    errors, to_update = validate_task_update(data)
    
    if errors:
        return jsonify({'error': 'Validation failed', 'details': errors}), 400
    
    if not to_update:
        return jsonify({'error': 'No fields to update'}), 400
    
    updated_task = update_task(task_id, to_update)
    
    return jsonify(updated_task), 200