from datetime import date
from backend.app.models.tasks import tasks, engine
from backend.app.validators.task_validator import validate_task
from sqlalchemy import desc

def create_task(task_data):
    if not validate_task(task_data):
        raise ValueError("Invalid task data")
    
    with engine.begin() as conn:
        insert_statement = tasks.insert().values(
            title=task_data['title'],
            priority=task_data['priority'],
            completed=task_data['completed'],
            description=task_data.get('description', ''),
            date=date.today()
        )
        result = conn.execute(insert_statement)
        task_id = result.inserted_primary_key[0]
        
        select_statement = tasks.select().where(tasks.c.id == task_id)
        created_task = conn.execute(select_statement).fetchone()
        
        return build_task_response(created_task)

def get_tasks():
    with engine.begin() as conn:
        select_statement = tasks.select().order_by(desc(tasks.c.date), desc(tasks.c.id))
        result = conn.execute(select_statement).fetchall()
        return [build_task_response(task) for task in result]

def get_task(task_id):
    with engine.begin() as conn:
        select_statement = tasks.select().where(tasks.c.id == task_id)
        result = conn.execute(select_statement).fetchone()
        return build_task_response(result) if result else None

def update_task(task_id, task):
    with engine.begin() as conn:
        select_statement = tasks.select().where(tasks.c.id == task_id)
        result = conn.execute(select_statement).fetchone()
        if not result:
            return None
        update_statement = tasks.update().where(tasks.c.id == task_id).values(**task)
        result = conn.execute(update_statement)
        return build_task_response(result) if result else None

def delete_task(task_id):
    with engine.begin() as conn:
        delete_statement = tasks.delete().where(tasks.c.id == task_id)
        result = conn.execute(delete_statement)
        return build_task_response(result) if result else None

def build_task_response(task):
    return {
        'id': task['id'],
        'title': task['title'],
        'description': task['description'] if task['description'] else None,
        'priority': task['priority'],
        'completed': task['completed'],
        'date': task['date'].isoformat() if task['date'] else None
    }