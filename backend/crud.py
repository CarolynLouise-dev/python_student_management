from typing import List, Optional
from models.student import Student
from sqlalchemy.orm import Session
from schemas.student import StudentCreate, StudentUpdate


# ===== CRUD =====
def get_all_students(db: Session) -> Optional[List[dict]]:
    try:
        students = db.query(Student).all()
        return students
    except Exception as e:
        print(f"Error loading students: {e}")
        return None


def get_student_by_mssv(mssv: str, db: Session) -> Optional[dict]:
    try:
        student = db.query(Student).filter(Student.mssv == mssv).first()
        if student:
            return student
        else:
            return None
    except Exception as e:
        print(f"Error loading student: {e}")
        return None


def add_student(student: StudentCreate, db: Session) -> dict:
    # status: success, conflict, error
    result = {
        "message": None,
        "status": "success",
        "error": None
    }
    try:
        exist = db.query(Student).filter(Student.mssv == student.mssv).first()
        if exist:
            result['status'] = 'conflict'
            result['error'] = "MSSV đã tồn tại"
        else:
            new_student = Student(**student.model_dump())
            db.add(new_student)
            db.commit()
            result['message'] = "Thêm thành công"
        return result
    except Exception as e:
        print(f"Error adding student: {e}")
        result['status'] = 'error'
        result['error'] = "Xảy ra lỗi khi thêm student"
        return result


def update_student(mssv: str, student: StudentUpdate, db: Session) -> dict:
    # status: success, notfound, error
    result = {
        "message": None,
        "status": "success",
        "error": None
    }
    try:
        exist = db.query(Student).filter(Student.mssv == mssv).first()
        if exist:
            # Cập nhật từng field từ schema vào instance hiện có
            update_data = student.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                # Chỉ gán những field thực sự tồn tại trên model
                if hasattr(exist, field):
                    setattr(exist, field, value)

            db.commit()
            db.refresh(exist)
            result['message'] = "Cập nhật thành công"
            return result
        else:
            result['error'] = "Không tìm thấy sinh viên"
            result['status'] = 'notfound'
            return result
    except Exception as e:
        print(f"Error updating student: {e}")
        result['status'] = 'error'
        result['message'] = "Xảy ra lỗi khi sửa thông tin student"
        return result


def delete_student(mssv: str, db: Session) -> dict:
    # status: success, notfound, error
    result = {
        "message": None,
        "status": "success",
        "error": None
    }
    try:
        exist = db.query(Student).filter(Student.mssv == mssv).first()
        if exist:
            db.delete(exist)
            db.commit()
            result['message'] = "Xóa thành công"
            return result
        else:
            result['error'] = "Không tìm thấy sinh viên"
            result['status'] = 'notfound'
            return result
    except Exception as e:
        print(f"Error deleting student: {e}")
        result['status'] = 'error'
        result['message'] = "Xảy ra lỗi khi xóa student"
        return result


def get_students_paginated(page: int = 1, limit: int = 15, search: Optional[str] = None, db: Session = None) -> dict:
    # status: success, error
    result = {
        "status": "success",
        "total": 0,
        "data": []
    }
    try:
        # lấy danh sách sinh viên phân trang có search tên hoặc mssv
        if search:
            all_students = db.query(Student).filter(
                    Student.mssv.like(f"%{search.strip()}%")|
                    Student.first_name.like(f"%{search.strip()}%")|
                    Student.last_name.like(f"%{search.strip()}%")
            )
            total = all_students.count()
            students = all_students.offset((page - 1) * limit).limit(limit).all()
        else:
            all_students = db.query(Student)
            total = all_students.count()
            students = all_students.offset((page - 1) * limit).limit(limit).all()
        result['total'] = total
        result['data'] = students
        return result
    except Exception as e:
        print(f"Error paginating students: {e}")
        result['status'] = 'error'
        return result
