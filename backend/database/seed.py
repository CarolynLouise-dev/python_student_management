import json
import pandas as pd
import models.student as model
from database.database import Base, SessionLocal, engine

def init_db():
    Base.metadata.create_all(engine)

def seed_db():
    Base.metadata.create_all(engine)
    db = SessionLocal()
    with open("data/student-scores.json", "r") as f:
        data = json.load(f)
        df = pd.DataFrame(data)
        # thêm cột id tự tăng từ 1
        df['id'] = range(1, len(df) + 1)

        for index, row in df.iterrows():
            exists = db.query(model.Student).filter(model.Student.id == row['id']).first()
            if exists:
                continue
            student = model.Student(
                **row.to_dict()
            )
            db.add(student)

    db.commit()
    db.close()