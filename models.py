from sqlalchemy import Column, Float, Integer, String
from database import Base

class StudentModel(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    course = Column(String, nullable=False)
    grade = Column(Float, nullable=False)
    year = Column(Integer, nullable=False)