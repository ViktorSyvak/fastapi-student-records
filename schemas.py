from pydantic import BaseModel, Field, ConfigDict


class Student(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=16, le=100)
    course: str = Field(min_length=2, max_length=100)
    grade: float = Field(ge=0.0, le=4.0)
    year: int = Field(ge=1, le=4)


class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    course: str
    grade: float
    year: int

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)

class UserResponse(BaseModel):
    id: int
    username: str 
    is_admin: bool 

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str