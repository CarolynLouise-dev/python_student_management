import random
import numpy as np
import json

FIRST_NAMES = ["An", "Binh", "Chi", "Dung", "Huy", "Khanh", "Linh", "My", "Nam", "Trang"]
LAST_NAMES = ["Nguyen", "Tran", "Le", "Pham", "Hoang", "Vu", "Dang", "Bui"]

STEM_CAREERS = [
    "Doctor", "Scientist", "Software Engineer",
    "Engineer", "Game Developer", "Construction Engineer"
]

NON_STEM_CAREERS = [
    "Lawyer", "Teacher", "Business Owner",
    "Writer", "Designer", "Business Analyst",
    "Banker", "Accountant"
]


def random_score(low, high, std=6):
    return int(np.clip(np.random.normal((low + high) / 2, std), low, high))


def maybe_score(prob_null, low, high):
    """Sinh điểm với xác suất null tự nhiên"""
    if random.random() < prob_null:
        return None
    return random_score(low, high)


def generate_student(idx):
    # -----------------------
    # 1. Gender → STEM bias
    # -----------------------
    gender = random.choice(["male", "female"])
    is_stem = random.random() < (0.65 if gender == "male" else 0.35)

    # -----------------------
    # 2. Ability
    # -----------------------
    ability = random.choices(
        ["high", "medium", "low"],
        weights=[0.3, 0.5, 0.2]
    )[0]

    # -----------------------
    # 3. Hành vi thực tế
    # -----------------------
    part_time_job = random.random() < (0.7 if ability == "low" else 0.3)
    absence_days = random.randint(10, 18) if ability == "low" else random.randint(1, 6)

    if is_stem:
        extracurricular = random.random() < 0.25
        self_study = random.randint(28, 42) if ability != "low" else random.randint(12, 20)
    else:
        extracurricular = random.random() < 0.7
        self_study = random.randint(10, 18) if ability != "low" else random.randint(5, 12)

    # -----------------------
    # 4. Range điểm nền
    # -----------------------
    if ability == "high":
        stem_range = (85, 98)
        social_range = (80, 92)
    elif ability == "medium":
        stem_range = (68, 84)
        social_range = (65, 80)
    else:
        stem_range = (45, 65)
        social_range = (45, 62)

    # -----------------------
    # 5. Sinh điểm (NULL tự nhiên)
    # -----------------------
    if is_stem:
        # STEM mạnh → hiếm null
        math = maybe_score(0.05, *stem_range)
        physics = maybe_score(0.05, *stem_range)
        chemistry = maybe_score(0.05, *stem_range)
        biology = maybe_score(0.05, *stem_range)

        # Xã hội yếu → dễ null
        history = maybe_score(0.35, 45, 65)
        geography = maybe_score(0.35, 45, 65)
        english = maybe_score(0.35, 45, 65)
    else:
        # Xã hội mạnh
        history = maybe_score(0.05, *social_range)
        geography = maybe_score(0.05, *social_range)
        english= maybe_score(0.05, *social_range)

        # STEM yếu → dễ null
        math = maybe_score(0.35, 45, 65)
        physics = maybe_score(0.45, 40, 60)
        chemistry = maybe_score(0.35, 45, 60)
        biology = maybe_score(0.30, 45, 65)

    # -----------------------
    # 6. Penalty hành vi xấu
    # -----------------------
    penalty = 0
    if part_time_job:
        penalty += random.randint(2, 5) if ability != "low" else random.randint(3, 7)

    if absence_days > 10:
        penalty += random.randint(3, 6) if ability != "low" else random.randint(5, 9)
    def apply_penalty(score):
        if score is None:
            return None
        return max(0, score - penalty)

    math = apply_penalty(math)
    physics = apply_penalty(physics)
    chemistry = apply_penalty(chemistry)
    biology = apply_penalty(biology)
    history = apply_penalty(history)
    geography = apply_penalty(geography)
    english = apply_penalty(english)

    # -----------------------
    # 7. Nghề nghiệp
    # -----------------------
    if is_stem:
        relevant_scores = [math, physics, chemistry, biology]
    else:
        relevant_scores = [history, geography, english]

    relevant_scores = [s for s in relevant_scores if s is not None]
    avg_relevant = np.mean(relevant_scores) if relevant_scores else 0
    min_score = 50 if ability == "high" else 45 if ability == "medium" else 40
    if avg_relevant < min_score or len(relevant_scores) < 2:
        career = "Unknown"
    else:
        career = random.choice(STEM_CAREERS if is_stem else NON_STEM_CAREERS)

    # -----------------------
    # 8. Output
    # -----------------------
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)

    return {
        "mssv": f"SV{idx:04d}",
        "first_name": first,
        "last_name": last,
        "email": f"{first.lower()}.{last.lower()}{idx}@gslingacademy.com",
        "gender": gender,
        "is_stem": is_stem,
        "part_time_job": part_time_job,
        "absence_days": absence_days,
        "extracurricular_activities": extracurricular,
        "weekly_self_study_hours": float(self_study),
        "career_aspiration": career,
        "math_score": math,
        "physics_score": physics,
        "chemistry_score": chemistry,
        "biology_score": biology,
        "history_score": history,
        "geography_score": geography,
        "english_score": english
    }

def generate_dataset(n=1000):
    return [generate_student(i + 1) for i in range(n)]


if __name__ == "__main__":
    dataset = generate_dataset(1000)
    with open("cleaned_student.json", "w") as f:
        json.dump(dataset, f, indent=4)
