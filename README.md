# FastAPI Student Records

Building a simple Student Records API with Python and FastAPI, supporting create, read, update and delete operations.

## Features

- Create student records
- View all students
- View a student by ID
- Update student records
- Delete student records
- Data validation with Pydantic
- Interactive API documentation with Swagger UI
- Persistent student records using SQLite
- Input validation for student data using Pydantic
- Filter students by course, year and minimum grade
- Structured API responses using Pydantic response models
- Improved HTTP status codes for create and delete operations
- Automated API testing with pytest
- Separate in-memory SQLite database for automated tests
- Modular FastAPI project structure
- Separate routers, schemas, database configuration and models 

## Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- SQLite
- SQLAlchemy
- pytest

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API home |
| GET | `/students` | Get all students |
| GET | `/students/{student_id}` | Get a student by ID |
| POST | `/students` | Create a student |
| PUT | `/students/{student_id}` | Update a student |
| DELETE | `/students/{student_id}` | Delete a student |

## Run Locally

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
fastapi dev main.py
```

Open the interactive API documentation at:

http://127.0.0.1:8000/docs

## Current Version

## Current Version

Version 7 refactors the Student Records API into a cleaner modular project structure.

The project is now separated into:

- `main.py` - FastAPI application setup
- `database.py` - Database connection and session management
- `models.py` - SQLAlchemy database models
- `schemas.py` - Pydantic request and response schemas
- `routers/students.py` - Student API routes
- `tests/test_main.py` - Automated pytest tests

The refactor improves maintainability and makes the project easier to extend.

Run the tests with:

```bash
python -m pytest -v
```

## Version History

- v1.0.0 - In-memory student records using a Python dictionary
- v2.0.0 - Persistent storage using SQLite and SQLAlchemy
- v3.0.0 - Student input validation using Pydantic
- v4.0.0 - Student filtering using FastAPI query parameters
- v5.0.0 - Response models and improved HTTP status codes
- v6.0.0 - Automated API testing with pytest
- v7.0.0 - Refactored project into a modular FastAPI structure