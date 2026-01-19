import json
from typing import List, Optional
from models.student import Student
import random
from datetime import datetime, timedelta

DATA_FILE = "data/students.json"


def random_date(start_year=1998, end_year=2006):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")


def maybe_none(value, empty_rate=0.25):
    """25% khả năng bị trống"""
    return None if random.random() < empty_rate else value


def generate_100_students():
    students = []

    ho_list = [
        "Nguyen", "Tran", "Le", "Pham", "Hoang", "Vo", "Do", "Dang", "Bui", "Huynh",
        "Kim", "Park", "Lee", "Choi", "Jung",
        "Wang", "Chen", "Zhang", "Liu", "Zhao", "Yang", "Huang",
        "Tanaka", "Suzuki", "Sato", "Takahashi", "Watanabe",
        "Smith", "Brown", "Johnson", "Miller", "Davis", "Wilson", "Moore",
        "Garcia", "Martinez", "Lopez", "Gonzalez", "Hernandez",
        "Dupont", "Martin", "Bernard", "Dubois",
        "Muller", "Schmidt", "Fischer", "Weber",
        "Rossi", "Bianchi", "Romano",
        "Singh", "Patel", "Sharma",
        "Khan", "Ali", "Hassan"
    ]

    ten_list = [
        # Việt Nam
        "An", "Binh", "Minh", "Long", "Linh", "Huy", "Phuc", "Khanh", "Trang", "Thao",
        "Nam", "Tuan", "Hung", "Duc", "Vy", "Nhi", "Tien", "Phong",

        # Quốc tế
        "Anna", "John", "David", "Emma", "Sophia", "Daniel", "Maria", "Michael",
        "James", "Emily", "Olivia", "Lucas", "Noah", "Ethan", "Ava", "Mia",

        # Hàn
        "Jisoo", "Minji", "Hoseok", "Taehyung", "Jungkook", "Hyunwoo",

        # Nhật
        "Haruto", "Yuki", "Sakura", "Ren", "Aiko", "Takumi",

        # Trung
        "Wei", "Jing", "Hao", "Yifan", "Xinyi", "Meilin",

        # Ấn
        "Arjun", "Riya", "Amit", "Priya", "Rahul",

        # Trung Đông
        "Omar", "Yusuf", "Aisha", "Fatima", "Zain"
    ]

    que_quan_list = [
        # Việt Nam
        "Hà Nội", "TP.HCM", "Đà Nẵng", "Huế", "Cần Thơ", "Nha Trang",
        "Hải Phòng", "Quảng Ninh", "Bình Dương", "Đồng Nai",

        # Châu Á
        "Seoul, Korea", "Busan, Korea",
        "Tokyo, Japan", "Osaka, Japan", "Kyoto, Japan",
        "Beijing, China", "Shanghai, China", "Shenzhen, China",
        "Bangkok, Thailand", "Chiang Mai, Thailand",
        "Singapore",
        "Kuala Lumpur, Malaysia",
        "Jakarta, Indonesia",
        "Manila, Philippines",
        "New Delhi, India", "Mumbai, India",
        "Dhaka, Bangladesh",

        # Châu Âu
        "London, UK", "Manchester, UK",
        "Paris, France", "Lyon, France",
        "Berlin, Germany", "Munich, Germany",
        "Rome, Italy", "Milan, Italy",
        "Madrid, Spain", "Barcelona, Spain",
        "Amsterdam, Netherlands",
        "Zurich, Switzerland",

        # Mỹ - Úc
        "New York, USA", "Los Angeles, USA", "San Francisco, USA",
        "Chicago, USA", "Boston, USA",
        "Toronto, Canada", "Vancouver, Canada",
        "Sydney, Australia", "Melbourne, Australia",

        # Trung Đông
        "Dubai, UAE", "Abu Dhabi, UAE",
        "Doha, Qatar",
        "Riyadh, Saudi Arabia"
    ]

    for i in range(1, 101):
        ho = random.choice(ho_list)
        ten = random.choice(ten_list)

        email = f"{ten.lower()}{i}@gmail.com"

        student = {
            "mssv": f"SV{i:03}",
            "ho": ho,
            "ten": ten,
            "email": maybe_none(email),
            "ngay_sinh": maybe_none(random_date()),
            "que_quan": maybe_none(random.choice(que_quan_list)),
            "diem_toan": maybe_none(round(random.uniform(4, 10), 1)),
            "diem_van": maybe_none(round(random.uniform(4, 10), 1)),
            "diem_anh": maybe_none(round(random.uniform(4, 10), 1)),
        }

        students.append(student)

    return students

# ===== FILE UTILS =====
def load_students():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

            # 👉 nếu file rỗng → auto tạo 100 SV
            if len(data) == 0:
                data = generate_100_students()
                save_students(data)

            return data

    except (FileNotFoundError, json.JSONDecodeError):
        # 👉 nếu chưa có file → tạo mới luôn
        data = generate_100_students()
        save_students(data)
        return data



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

