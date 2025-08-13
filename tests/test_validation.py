from backend.app.validators.task_validator import validate_task, validate_task_update

def test_valid_task():
    valid_task = {
        'title': 'Test Task',
        'description': 'This is a test task',
        'priority': 2,
        'completed': False,
    }
    assert validate_task(valid_task) == True

def test_invalid_title():
    invalid_task = {
        'title': '',
        'description': 'This is a test task',
        'priority': 2,
        'completed': False,
    }
    assert validate_task(invalid_task) == False

def test_invalid_priority():
    invalid_task = {
        'title': 'Test Task',
        'description': 'This is a test task',
        'priority': 6,
        'completed': False,
    }
    assert validate_task(invalid_task) == False

def test_invalid_completed():
    invalid_task = {
        'title': 'Test Task',
        'description': 'This is a test task',
        'priority': 2,
        'completed': 'True',
    }
    assert validate_task(invalid_task) == False

def test_invalid_description():
    invalid_task = {
        'title': 'Test Task',
        'description': 123,
        'priority': 2,
        'completed': False,
    }
    assert validate_task(invalid_task) == False

def test_invalid_type():
    invalid_task = {
        'title': 'Test Task',
        'description': 'This is a test task',
        'priority': '2',
        'completed': False,
    }
    assert validate_task(invalid_task) == False

def test_empty_task():
    invalid_task = {}
    assert validate_task(invalid_task) == False

def test_valid_task_update():
    valid_task = {
        'title': 'Test Task',
        'description': 'This is a test task',
        'priority': 2,
        'completed': False,
    }
    assert validate_task_update(valid_task) == ([], valid_task)
