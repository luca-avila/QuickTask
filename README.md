# QuickTask API

A RESTful task management API built with Flask and SQLAlchemy, featuring comprehensive validation, error handling, and a clean service layer architecture. This project demonstrates modern backend development practices with proper testing and documentation.

## 🚀 Features

- **CRUD Operations**: Complete Create, Read, Update, and Delete functionality for tasks
- **Data Validation**: Comprehensive input validation with detailed error messages
- **Service Layer Architecture**: Clean separation of business logic from routes
- **Database Integration**: SQLite with SQLAlchemy ORM for data persistence
- **CORS Support**: Ready for frontend integration
- **Error Handling**: Proper HTTP status codes and error responses
- **Testing**: Comprehensive test suite with pytest
- **RESTful Design**: Follows REST API conventions

## 🛠️ Tech Stack

- **Backend Framework**: Flask 3.1.1
- **Database**: SQLite with SQLAlchemy 1.4.27
- **Validation**: Custom validation layer
- **CORS**: Flask-CORS for cross-origin requests
- **Testing**: pytest for comprehensive testing
- **Architecture**: Service layer pattern with clean separation of concerns

## 📋 API Endpoints

### Tasks

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| `POST` | `/tasks` | Create a new task | 201 (Created) |
| `GET` | `/tasks` | Get all tasks (ordered by date and ID) | 200 (OK) |
| `GET` | `/tasks/<id>` | Get a specific task by ID | 200 (OK) |
| `PATCH` | `/tasks/<id>` | Update a task (partial update) | 200 (OK) |
| `DELETE` | `/tasks/<id>` | Delete a task | 204 (No Content) |

### Task Schema

```json
{
  "title": "string (1-200 chars, required)",
  "description": "string (optional, max 1000 chars)",
  "priority": "integer (0-5, required)",
  "completed": "boolean (required)"
}
```

### Response Schema

```json
{
  "id": "integer (auto-generated)",
  "title": "string",
  "description": "string or null",
  "priority": "integer",
  "completed": "boolean",
  "date": "string (ISO format)"
}
```

## 🏗️ Project Structure

```
QuickTask/
├── backend/
│   └── app/
│       ├── models/          # Database models and schema
│       ├── routes/          # API endpoints and routing
│       ├── services/        # Business logic layer
│       ├── validators/      # Input validation logic
│       └── config.py        # Application configuration
├── tests/                   # Test suite
│   ├── test_api.py         # API endpoint tests
│   └── test_validation.py  # Validation logic tests
├── frontend/               # Frontend (coming soon)
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── pytest.ini             # Pytest configuration
└── README.md              # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd QuickTask
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5000`

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

## 📝 API Examples

### Create a Task

```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete portfolio project",
    "description": "Finish the QuickTask API and add authentication",
    "priority": 5,
    "completed": false
  }'
```

**Response:**
```json
{
  "id": 1,
  "title": "Complete portfolio project",
  "description": "Finish the QuickTask API and add authentication",
  "priority": 5,
  "completed": false,
  "date": "2024-01-15"
}
```

### Get All Tasks

```bash
curl http://localhost:5000/tasks
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Complete portfolio project",
    "description": "Finish the QuickTask API and add authentication",
    "priority": 5,
    "completed": false,
    "date": "2024-01-15"
  }
]
```

### Update a Task

```bash
curl -X PATCH http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

**Response:**
```json
{
  "id": 1,
  "title": "Complete portfolio project",
  "description": "Finish the QuickTask API and add authentication",
  "priority": 5,
  "completed": true,
  "date": "2024-01-15"
}
```

### Delete a Task

```bash
curl -X DELETE http://localhost:5000/tasks/1
```

**Response:** 204 No Content

## 🔧 Development

### Database

The application uses SQLite with automatic table creation. The database file is located at `backend/database.db` and is created automatically when the application starts.

### Validation

All input is validated through a custom validation layer that ensures:
- **Title**: 1-200 characters, required
- **Description**: Optional, max 1000 characters
- **Priority**: Integer between 0-5, required
- **Completed**: Boolean value, required

### Error Handling

The API returns appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `204` - No Content (for deletions)
- `400` - Bad Request (validation errors)
- `404` - Not Found
- `500` - Internal Server Error

### Testing

The project includes comprehensive tests covering:
- **API endpoints** - All CRUD operations
- **Validation logic** - Input validation
- **Error cases** - Invalid data handling
- **Edge cases** - Boundary conditions

Run tests with:
```bash
pytest -v
```

## 🧪 Testing Strategy

The project uses a comprehensive testing approach:

### Test Coverage
- **API Endpoints**: All CRUD operations tested
- **Validation**: Input validation logic tested
- **Error Handling**: Error responses verified

### Test Structure
```python
def test_create_task():
    # Setup
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()
    
    # Test data
    task_data = {
        'title': 'Test Task',
        'priority': 3,
        'completed': False
    }
    
    # Execute
    response = client.post('/tasks', json=task_data)
    
    # Assert
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Test Task'
```

## 👨‍💻 Author

Built as part of a portfolio project to demonstrate full-stack development skills, including:
- Backend API development with Flask
- Database design and integration
- Testing and validation
- Documentation and best practices

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

This is a portfolio project, but suggestions and improvements are welcome!

## 📞 Contact

For questions or feedback about this project, please reach out through the project repository.