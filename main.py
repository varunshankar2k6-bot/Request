from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import Student, StudentProfile
from schemas import (
    StudentCreate,
    StudentProfileCreate,
    StudentResponse
)

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/students", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    db_student = Student(
        name=student.name,
        email=student.email
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


@app.post("/students/{student_id}/profile")
def create_profile(
    student_id: int,
    profile: StudentProfileCreate,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        return {"error": "Student not found"}

    db_profile = StudentProfile(
        address=profile.address,
        phone=profile.phone,
        student_id=student_id
    )

    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    return db_profile


@app.get(
    "/students/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    return student