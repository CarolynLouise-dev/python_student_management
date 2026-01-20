import json
from typing import List, Optional
from models.student import Student
import random
from datetime import datetime, timedelta

DATA_FILE = "data/student-scores.json"


# ===== FILE UTILS =====
def load_students():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_students(students):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=4)


# ===== CRUD =====
def get_all_students() -> List[dict]:
    return load_students()

def get_student_by_mssv(mssv: str) -> Optional[dict]:
    for s in load_students():
        if s.get("mssv") == mssv:
            return s
    return None

def add_student(student: Student) -> bool:
    students = load_students()

    # kiểm tra trùng MSSV
    if any(s.get("mssv") == student.mssv for s in students):
        return False

    students.append(student.dict())
    save_students(students)
    return True

def update_student(mssv: str, student: Student) -> bool:
    students = load_students()

    for i, s in enumerate(students):
        if s.get("mssv") == mssv:
            students[i] = student.dict()
            save_students(students)
            return True

    return False

def delete_student(mssv: str) -> bool:
    students = load_students()
    new_students = [s for s in students if s.get("mssv") != mssv]

    if len(new_students) == len(students):
        return False

    save_students(new_students)
    return True

def paginate_students(
    students: List[dict],
    page: int = 1,
    limit: int = 15
):
    total = len(students)

    start = (page - 1) * limit
    end = start + limit

    return {
        "data": students[start:end],
        "total": total,
        "page": page,
        "limit": limit
    }

def get_students_paginated(
    page: int = 1,
    limit: int = 15,
    search: Optional[str] = None
):
    students = load_students()
    # ===== SEARCH =====
    if search:
        keyword = search.strip().lower()
        students = [
            s for s in students
            if keyword in s.get("mssv", "").lower()
            or keyword in s.get("ten", "").lower()
        ]

    total = len(students)

    start = (page - 1) * limit
    end = start + limit

    return {
        "data": students[start:end],
        "total": total
    }