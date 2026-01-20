import random
import json

random.seed(99)

first_names = ["Alex", "Linda", "Michael", "Sara", "David", "Emily", "John", "Anna"]
last_names = ["Brown", "Nguyen", "Lee", "Wilson", "Tran", "Smith", "Kim", "Garcia"]
careers = ["Engineer", "Doctor", "Accountant", "Business Analyst", "Teacher"]

def random_score():
    return random.randint(55, 100)

students = []

for mssv in range(2001, 2124):
    absence_days = random.randint(0, 15)
    extracurricular = random.choice([True, False])
    part_time = random.choice([True, False])

    student = {
        "mssv": mssv,
        "first_name": random.choice(first_names),
        "last_name": random.choice(last_names),
        "email": f"student.{mssv}@gslingacademy.com",
        "gender": random.choice(["male", "female"]),
        "part_time_job": part_time,
        "absence_days": absence_days,
        "extracurricular_activities": extracurricular,
        "weekly_self_study_hours": round(random.uniform(5, 40), 1),
        "career_aspiration": random.choice(careers),
        "math_score": random_score(),
        "history_score": random_score(),
        "physics_score": random_score(),
        "chemistry_score": random_score(),
        "biology_score": random_score(),
        "english_score": random_score(),
        "geography_score": random_score()
    }

    # 🔥 EMAIL – thiếu rất nhiều (MCAR)
    if random.random() < 0.4:
        student["email"] = None

    # 🔥 CAREER – rất hay thiếu (MAR + MNAR)
    if absence_days > 5 and random.random() < 0.7:
        student["career_aspiration"] = None
    elif random.random() < 0.3:
        student["career_aspiration"] = None

    # 🔥 WEEKLY STUDY – không đi làm mới hay khai
    if part_time and random.random() < 0.6:
        student["weekly_self_study_hours"] = None

    # 🔥 CHEMISTRY – môn bị giấu nhiều nhất (MNAR)
    if student["chemistry_score"] < 75 and random.random() < 0.8:
        student["chemistry_score"] = None
    elif random.random() < 0.3:
        student["chemistry_score"] = None

    # 🔥 PHYSICS – missing theo cụm
    if mssv % 4 == 0 or random.random() < 0.25:
        student["physics_score"] = None

    # 🔥 HISTORY – không ngoại khóa hay thiếu
    if not extracurricular and random.random() < 0.5:
        student["history_score"] = None

    # 🔥 GEOGRAPHY – random nhưng nhiều
    if random.random() < 0.3:
        student["geography_score"] = None

    # 🔥 BONUS: sinh viên cực lười khai 😴
    if absence_days > 10:
        for key in ["biology_score", "english_score"]:
            if random.random() < 0.5:
                student[key] = None

    students.append(student)

# In thử 2 record đầu
for s in students[:123]:
    print(json.dumps(s, indent=4))
