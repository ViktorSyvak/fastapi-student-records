from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Student Records System",
    description="This is a simple API for managing student records.",
    version="1.0.0"
)

class Student(BaseModel):
    name: str
    age: int
    course: str
    grade: float
    year: int

students = {
    1: {
        "name": "John Smith",
        "age": 23,
        "course": "Computer Science",
        "grade": 3.2,
        "year": 4
    },
    2: {
        "name": "Sam Jones",
        "age": 28,
        "course": "Software Development",
        "grade": 3.7,
        "year": 1
    }
} 

@app.get("/")
def home():
    return {
        "message": "Student Records Systems API"
    }


@app.get("/students")
def get_students():
    return students

@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return students[student_id]

@app.post("/students")
def create_student(student: Student): 
    new_id = max(students.keys(), default=0) + 1

    students[new_id] = student.model_dump()

    return {
        "student_id": new_id,
        "student": students[new_id]
    }

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):

    if student_id not in students: 
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    students[student_id] = student.model_dump()

    return {
        "message": "Student updated successfully",
        "student_id": student_id,
        "student": students[student_id]
    }

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    deleted_student = students.pop(student_id)
    return {
        "message": "Student deleted successfully",
        "student_id": student_id,
        "student": deleted_student
    }