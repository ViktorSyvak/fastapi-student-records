from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import Student, StudentResponse


router = APIRouter(tags=["students"])


@router.get("/students", response_model=list[StudentResponse])
def get_students(
    course: str | None = None,
    year: int | None = Query(default=None, ge=1, le=4),
    min_grade: float | None = Query(default=None, ge=0.0, le=4.0),
    db: Session = Depends(get_db)
):

    query = db.query(models.StudentModel)

    if course:
        query = query.filter(
            models.StudentModel.course.ilike(f"%{course}%")
        )

    if year is not None:
        query = query.filter(
            models.StudentModel.year == year
        )

    if min_grade is not None:
        query = query.filter(
            models.StudentModel.grade >= min_grade
        )

    return query.all()


@router.get("/students/{student_id}", response_model=StudentResponse)
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


@router.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
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


@router.put(
    "/students/{student_id}",
    response_model=StudentResponse
)
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

    return existing_student


@router.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
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

    return Response(status_code=status.HTTP_204_NO_CONTENT)