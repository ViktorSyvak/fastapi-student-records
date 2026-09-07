from fastapi import FastAPI

from database import Base, engine
from routers.students import router as students_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Student Records System",
    description="This is a simple API for managing student records.",
    version="7.0.0"
)


app.include_router(students_router)


@app.get("/")
def home():
    return {
        "message": "Student Records System API"
    }