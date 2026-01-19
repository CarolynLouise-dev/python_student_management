from pydantic import BaseModel
from typing import Optional

class Student(BaseModel):
    mssv: str
    first_name: str
    last_name: str
    email: Optional[str] = None
    gender: Optional[str] = None
    part_time_job: Optional[bool] = None
    absence_days: Optional[int] = None
    extracurricular_activities: Optional[bool] = None
    weekly_self_study_hours: Optional[float] = None
    career_aspiration: Optional[str] = None
    math_score: Optional[int] = None
    history_score: Optional[int] = None
    physics_score: Optional[int] = None
    chemistry_score: Optional[int] = None
    biology_score: Optional[int] = None
    english_score: Optional[int] = None
    geography_score: Optional[int] = None
