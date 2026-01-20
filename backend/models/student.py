from database.database import Base
from sqlalchemy import Column, Float, String, Date, Integer, Boolean

class Student(Base):
    __tablename__ = "students_score"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    mssv: str = Column(String, index=True, nullable=True)
    first_name: str = Column(String, nullable=True)
    last_name: str = Column(String, nullable=True)
    email: str = Column(String, nullable=True)
    gender: str = Column(String, nullable=True)
    part_time_job: bool = Column(Boolean, nullable=True)
    absence_days: int = Column(Integer, nullable=True)
    extracurricular_activities: bool = Column(Boolean, nullable=True)
    weekly_self_study_hours: float = Column(Float, nullable=True)
    career_aspiration: str = Column(String, nullable=True)
    math_score: int = Column(Integer, nullable=True)
    history_score: int = Column(Integer, nullable=True)
    physics_score: int = Column(Integer, nullable=True)
    chemistry_score: int = Column(Integer, nullable=True)
    biology_score: int = Column(Integer, nullable=True)
    english_score: int = Column(Integer, nullable=True)
    geography_score: int = Column(Integer, nullable=True)