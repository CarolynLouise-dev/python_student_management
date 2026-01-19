from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

from models import Student
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

# ===== ROOT =====
@app.get("/")
def root():
    return {"message": "API is running 🚀"}


# ===== STUDENTS =====
@app.get("/students")
def get_students(
    page: int = Query(1, ge=1),
    limit: int = Query(15, ge=1),
    search: Optional[str] = None
):
    result = crud.get_students_paginated(page, limit, search)
    return {
        **result,
        "page": page,
        "limit": limit
    }

@app.get("/students/Allstudents")
def get_all_students():
    students = crud.get_all_students()
    return students

@app.get("/students/{mssv}")
def get_student(mssv: str):
    student = crud.get_student_by_mssv(mssv)
    if not student:
        raise HTTPException(status_code=404, detail="Không tìm thấy sinh viên")
    return student


@app.post("/students")
def create_student(student: Student):
    if not crud.add_student(student):
        raise HTTPException(status_code=400, detail="MSSV đã tồn tại")
    return {"message": "Thêm thành công"}


@app.put("/students/{mssv}")
def update_student(mssv: str, student: Student):
    if crud.update_student(mssv, student):
        return {"message": "Cập nhật thành công"}
    return {"error": "Không tìm thấy sinh viên"}


@app.delete("/students/{mssv}")
def delete_student(mssv: str):
    if not crud.delete_student(mssv):
        raise HTTPException(status_code=404, detail="Không tìm thấy sinh viên")
    return {"message": "Xóa thành công"}
