from fastapi import FastAPI, Query, HTTPException, status, Depends
from typing import Optional
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database.database import get_db
from database.seed import seed_db
from models.student import Student
from schemas.student import StudentCreate, StudentGet, StudentUpdate
import crud

app = FastAPI(title="Student Management API")

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

seed_db()

# ===== ROOT =====
@app.get("/")
def root():
    return {"message": "API is running 🚀"}


# ===== STUDENTS =====
@app.get("/students",status_code=status.HTTP_200_OK)
def get_students(
    page: int = Query(1, ge=1),
    limit: int = Query(15, ge=1),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    result = crud.get_students_paginated(page, limit, search, db)
    if result['status']=='error':
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "page": page,
                "limit": limit,
                **result
            }
        )
    else:
        return {
            **result,
            "page": page,
            "limit": limit
        }

@app.get("/students/Allstudents")
def get_all_students(db: Session = Depends(get_db)):
    students = crud.get_all_students(db)
    if not students:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=[]
        )
    return students

@app.get("/students/{mssv}")
def get_student(mssv: str, db: Session = Depends(get_db)):
    student = crud.get_student_by_mssv(mssv, db)
    if not student:
        raise HTTPException(status_code=404, detail="Không tìm thấy sinh viên")
    return student

@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    result = crud.add_student(student, db)
    if result['status'] == "error":
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = result
        )
    elif result['status'] == "conflict":
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=result
        )
    return result


@app.put("/students/{mssv}", response_model=None, status_code=status.HTTP_202_ACCEPTED)
def update_student(mssv: str, student: StudentUpdate, db: Session = Depends(get_db)):
    result = crud.update_student(mssv, student, db)
    if result['status'] == "success":
        return result
    elif result['status'] == "notfound":
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=result
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=result
    )

@app.delete("/students/{mssv}", response_model=None, status_code=status.HTTP_200_OK)
def delete_student(mssv: str, db: Session = Depends(get_db)):
    result = crud.delete_student(mssv, db)
    if result['status'] == "success":
        return result
    elif result['status'] == "notfound":
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=result
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=result
    )



