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

## Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- SQLite
- SQLAlchemy

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

Version 3 adds Pydantic input validation to ensure student records contain valid names, ages, courses, grades and study years.

Validation rules include:

- Name: 2–100 characters
- Age: 16–100
- Course: 2–100 characters
- Grade: 0.0–4.0
- Year: 1–4

## Version History

- v1.0.0 - In-memory student records using a Python dictionary
- v2.0.0 - Persistent storage using SQLite and SQLAlchemy
- v3.0.0 - Student input validation using Pydantic