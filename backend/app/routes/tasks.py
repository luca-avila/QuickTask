from datetime import date
from sqlalchemy import desc
from flask import Blueprint, request, jsonify
from backend.app.models.tasks import tasks, engine
from backend.app.validators.task_validator import validate_task, validate_task_update

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

    # Return error if task is not valid
    if not validate_task(data):
        return jsonify({'error': 'Invalid task'}), 400

    # Add to the database
    try:
        with engine.begin() as conn:
            insert_statement = tasks.insert().values(
            title = data['title'],
            priority = data['priority'],
            completed = data['completed'],
            description = data.get('description', ''),
            date = date.today()
            )
            conn.execute(insert_statement)
    except Exception as e:
        return jsonify({'error': f'Error adding task: {str(e)}'}), 500
    
    # Return success message
    return jsonify({'message': 'Task successfully added'}), 201

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

@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    # Get task
    try:
        with engine.begin() as conn:
            select_statement = tasks.select().where(tasks.c.id == task_id)
            result = conn.execute(select_statement).fetchone()
    except Exception as e:
        return jsonify({'error': f'Error getting task: {str(e)}'}), 500

    # Return error if task not found
    if not result:
        return jsonify({'error': 'Task not found'}), 404
    
    # Convert task to dictionary
    task_dict = build_task_response(result)

    return jsonify(task_dict), 200
    
@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Delete task
    try:
        with engine.begin() as conn:
            delete_statement = tasks.delete().where(tasks.c.id == task_id)
            result = conn.execute(delete_statement)
    except Exception as e:
        return jsonify({'error': f'Error deleting task: {str(e)}'}), 500

    # If no tasks were deleted, return error
    if result.rowcount == 0:
        return jsonify({'error': 'Task not found'}), 404

    # Return success message
    return jsonify({'message': 'Task deleted successfully'}), 200

@tasks_bp.route('/tasks/<int:task_id>', methods=['PATCH'])
def modify_task(task_id):
    data = request.json

    # Return error if no JSON received
    if data is None:
        return jsonify({'error': 'No JSON data received'}), 400

    # Check if task exists
    try:
        with engine.begin() as conn:
            select_statement = tasks.select().where(tasks.c.id == task_id)
            result = conn.execute(select_statement).fetchone()
    except Exception as e:
        return jsonify({'error': f'Error checking task: {str(e)}'}), 500

    # Return error if task not found
    if not result:
        return jsonify({'error': 'Task not found'}), 404

    # Validate update data
    errors, to_update = validate_task_update(data)
    
    if errors:
        return jsonify({'error': 'Validation failed', 'details': errors}), 400
    
    if not to_update:
        return jsonify({'error': 'No fields to update'}), 400
    
    # Update task in database
    try:
        with engine.begin() as conn:
            update_statement = tasks.update().where(tasks.c.id == task_id).values(**to_update)
            result = conn.execute(update_statement)
    except Exception as e:
        return jsonify({'error': f'Error updating task: {str(e)}'}), 500
    
    # Return success message
    return jsonify({'message': 'Task updated successfully'}), 200