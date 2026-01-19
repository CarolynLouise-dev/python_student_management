import csv
import json

INPUT_CSV = "student-scores.csv"
OUTPUT_JSON = "student-scores.json"

INT_FIELDS = {
    "mssv",  #  dùng mssv luôn
    "absence_days",
    "math_score",
    "history_score",
    "physics_score",
    "chemistry_score",
    "biology_score",
    "english_score",
    "geography_score",
}

FLOAT_FIELDS = {
    "weekly_self_study_hours",
}

BOOL_FIELDS = {
    "part_time_job",
    "extracurricular_activities",
}

def clean_value(key, value):
    if value is None or value.strip() == "":
        return None

    value = value.strip()

    if key in INT_FIELDS:
        try:
            return int(value)
        except ValueError:
            return None

    if key in FLOAT_FIELDS:
        try:
            return float(value)
        except ValueError:
            return None

    if key in BOOL_FIELDS:
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
        return None

    return value


with open(INPUT_CSV, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    students = []
    for row in reader:
        clean_row = {}

        for key, value in row.items():
            #  đổi id → mssv tại đây
            if key == "id":
                clean_row["mssv"] = clean_value("mssv", value)
            else:
                clean_row[key] = clean_value(key, value)

        students.append(clean_row)

with open(OUTPUT_JSON, "w", encoding="utf-8") as jsonfile:
    json.dump(students, jsonfile, ensure_ascii=False, indent=4)

print("✅ CSV → JSON thành công | id đã được đổi sang mssv | data sạch")
