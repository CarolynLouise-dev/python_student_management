from pydantic import BaseModel, EmailStr
from datetime import date

class StudentCreate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    gender: str | None = None
    part_time_job: bool | None = None
    absence_days: int | None = None
    extracurricular_activities: bool | None = None
    weekly_self_study_hours: float | None = None
    career_aspiration: str | None = None
    math_score: int | None = None
    history_score: int | None = None
    physics_score: int | None = None
    chemistry_score: int | None = None
    biology_score: int | None = None
    english_score: int | None = None
    geography_score: int | None = None

class StudentGet(StudentCreate):
    id: int
    mssv: str | None = None

    class Config:
        from_attributes = True # tự map attributes từ ORM object