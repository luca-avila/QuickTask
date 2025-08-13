import json
from run import create_app

def test_get_tasks():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()
    
    response = client.get('/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_create_task():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    task_data = {
        'title': 'Test Task',
        'description': 'This is a test task',
        'priority': 2,
        'completed': False
    }

    response = client.post('/tasks', json=task_data)
    assert response.status_code == 201
    data = json.loads(response.data)

    assert data['title'] == 'Test Task'
    assert data['description'] == 'This is a test task'
    assert data['priority'] == 2
    assert data['completed'] == False

    assert 'id' in data
    assert isinstance(data['id'], int)

def test_update_task():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    # Create a task
    create_data = {
        'title': 'Test Task',
        'description': 'This is a test task',
        'priority': 2,
        'completed': False
    }

    response = client.post('/tasks', json=create_data)
    assert response.status_code == 201
    data = json.loads(response.data)

    # Update the task
    update_data = {
        'title': 'Updated Task',
        'description': 'This is an updated task',
        'priority': 3,
        'completed': True
    }

    response = client.patch(f'/tasks/{data["id"]}', json=update_data)
    assert response.status_code == 200
    data = json.loads(response.data)

    # Check if the task was updated
    assert data['title'] == 'Updated Task'
    assert data['description'] == 'This is an updated task'
    assert data['priority'] == 3
    assert data['completed'] == True


def test_delete_task():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    # Create a task
    create_data = {
        'title': 'Test Task',
        'description': 'This is a test task',
        'priority': 2,
        'completed': False
    }

    response = client.post('/tasks', json=create_data)
    assert response.status_code == 201
    data = json.loads(response.data)

    # Delete the task
    response = client.delete(f'/tasks/{data["id"]}')
    assert response.status_code == 204

def test_get_task_by_id():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    # Create a task
    create_data = {
        'title': 'Test Task',
        'description': 'This is a test task',
        'priority': 2,
        'completed': False
    }

    response = client.post('/tasks', json=create_data)
    assert response.status_code == 201
    data = json.loads(response.data)

    # Get the task by id
    response = client.get(f'/tasks/{data["id"]}')
    assert response.status_code == 200
    data = json.loads(response.data)

    # Check if the task was returned
    assert data['title'] == 'Test Task'
    assert data['description'] == 'This is a test task'
    assert data['priority'] == 2
    assert data['completed'] == False
    