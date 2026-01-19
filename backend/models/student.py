from database.database import Base
from sqlalchemy import Column, Float, String, Date

class Student(Base):
    __tablename__ = "students"
    mssv: str = Column(String, primary_key=True, index=True, nullable=False)
    ho: str = Column(String, nullable=True)
    ten: str = Column(String, nullable=True)
    email: str = Column(String, nullable=True)
    ngay_sinh: Date = Column(Date, nullable=True)
    que_quan: str = Column(String, nullable=True)
    diem_toan: float = Column(Float, nullable=True)
    diem_van: float = Column(Float, nullable=True)
    diem_anh: float = Column(Float, nullable=True)
