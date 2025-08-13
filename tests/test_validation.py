from backend.app.validators.task_validator import validate_task

def test_valid_task():
    valid_task = {
        'title': 'Test Task',
        'description': 'This is a test task',
        'priority': 2,
        'completed': False,
    }
    assert validate_task(valid_task) == True