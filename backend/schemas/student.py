from pydantic import BaseModel, EmailStr
from datetime import date

class StudentCreate(BaseModel):
    ho: str | None = None
    ten: str | None = None
    email: EmailStr | None = None
    ngay_sinh: date | None = None
    que_quan: str | None = None
    diem_toan: float | None = None
    diem_van: float | None = None
    diem_anh: float | None = None

class StudentGet(StudentCreate):
    mssv: str

    class Config:
        from_attributes = True # tự map attributes từ ORM object