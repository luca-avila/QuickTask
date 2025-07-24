def validate_task(task):
    if not task['title'] or len(task['title']) > 200:
        return False
    if type(task['priority']) is not int:
        return False
    if type(task['completed']) is not bool:
        return False
    if task['priority'] < 0 or task['priority'] > 5:
        return False
    if task['description'] and len(task['description']) > 1000:
        return False
    return True

def validate_task_update(data):
    errors = []
    to_update = {}
    
    # Validate priority if provided
    if 'priority' in data:
        try:
            priority = int(data['priority'])
            if priority < 0 or priority > 5:
                errors.append('Priority must be between 0 and 5')
            else:
                to_update['priority'] = priority
        except (ValueError, TypeError):
            errors.append('Priority should be a number')
    
    # Validate completed if provided
    if 'completed' in data:
        if data['completed'] not in [True, False]:
            errors.append('Completed should be a boolean')
        else:
            to_update['completed'] = data['completed']
    
    # Validate title if provided
    if 'title' in data:
        if not data['title'] or len(data['title']) > 200:
            errors.append('Title must be between 1 and 200 characters')
        else:
            to_update['title'] = data['title']
    
    # Validate description if provided
    if 'description' in data:
        if data['description'] and len(data['description']) > 1000:
            errors.append('Description must be less than 1000 characters')
        else:
            to_update['description'] = data['description']
    
    return errors, to_update