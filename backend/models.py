from pydantic import BaseModel
from typing import Optional

class Student(BaseModel):
    mssv: str
    ho: Optional[str] = None
    ten: Optional[str] = None
    email: Optional[str] = None
    ngay_sinh: Optional[str] = None
    que_quan: Optional[str] = None
    diem_toan: Optional[float] = None
    diem_van: Optional[float] = None
    diem_anh: Optional[float] = None
