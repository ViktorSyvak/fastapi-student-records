from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

import models
from database import Base, engine, SessionLocal


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Student Records System",
    description="This is a simple API for managing student records.",
    version="4.0.0"
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


class Student(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=16, le=100)
    course: str = Field(min_length=2, max_length=100)
    grade: float = Field(ge=0.0, le=4.0)
    year: int = Field(ge=1, le=4)


@app.get("/")
def home():
    return {
        "message": "Student Records System API"
    }


@app.get("/students")
def get_students(
    course: str | None = None,
    year: int | None = Query(default=None, ge=1, le=4),
    min_grade: float | None = Query(default=None, ge=0.0, le=4.0),
    db: Session = Depends(get_db)
):

    query = db.query(models.StudentModel)

    if course: 
        query = query.filter(models.StudentModel.course.ilike(f"%{course}%")
        )

    if year is not None:
        query = query.filter(models.StudentModel.year == year
        )

    if min_grade is not None:
        query = query.filter(
            models.StudentModel.grade >= min_grade
        )

    return query.all()


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