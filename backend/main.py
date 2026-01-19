from fastapi import FastAPI, Query
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

from models import Student
import crud

app = FastAPI(title="Student Management API")

# ===== CORS (để FE HTML gọi được) =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # cho phép tất cả (dễ demo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== TEST =====
@app.get("/")
def root():
    return {"message": "API is running 🚀"}

# ===== CRUD SINH VIÊN =====

@app.get("/students")
def get_students(
    page: int = Query(1, ge=1),
    limit: int = Query(15, ge=1),
    search: Optional[str] = None
):
    result = crud.get_students_paginated(page, limit, search)
    return {
        **result,      # data, total
        "page": page,
        "limit": limit
    }

@app.get("/students/{mssv}")
def get_student(mssv: str):
    student = crud.get_student_by_mssv(mssv)
    if student:
        return student
    return {"error": "Không tìm thấy sinh viên"}


@app.post("/students")
def create_student(student: Student):
    if crud.add_student(student):
        return {"message": "Thêm thành công"}
    return {"error": "MSSV đã tồn tại"}


@app.put("/students/{mssv}")
def update_student(mssv: str, student: Student):
    if crud.update_student(mssv, student):
        return {"message": "Cập nhật thành công"}
    return {"error": "Không tìm thấy sinh viên"}


@app.delete("/students/{mssv}")
def delete_student(mssv: str):
    if crud.delete_student(mssv):
        return {"message": "Xóa thành công"}
    return {"error": "Không tìm thấy sinh viên"}

