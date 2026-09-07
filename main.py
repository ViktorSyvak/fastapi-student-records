from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

import models
from database import Base, engine, SessionLocal


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Student Records System",
    description="This is a simple API for managing student records.",
    version="2.0.0"
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


class Student(BaseModel):
    name: str
    age: int
    course: str
    grade: float
    year: int


@app.get("/")
def home():
    return {
        "message": "Student Records System API"
    }


@app.get("/students")
def get_students(db: Session = Depends(get_db)):

    students = db.query(models.StudentModel).all()

    return students


@app.get("/students/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(models.StudentModel).filter(
        models.StudentModel.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@app.post("/students")
def create_student(
    student: Student,
    db: Session = Depends(get_db)
):

    new_student = models.StudentModel(
        name=student.name,
        age=student.age,
        course=student.course,
        grade=student.grade,
        year=student.year
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    student: Student,
    db: Session = Depends(get_db)
):

    existing_student = db.query(models.StudentModel).filter(
        models.StudentModel.id == student_id
    ).first()

    if existing_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    existing_student.name = student.name
    existing_student.age = student.age
    existing_student.course = student.course
    existing_student.grade = student.grade
    existing_student.year = student.year

    db.commit()
    db.refresh(existing_student)

    return {
        "message": "Student updated successfully",
        "student": existing_student
    }


@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(models.StudentModel).filter(
        models.StudentModel.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully",
        "student_id": student_id
    }