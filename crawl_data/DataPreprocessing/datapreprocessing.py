import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ======================
# 1. LOAD DATA
# ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(os.path.dirname(BASE_DIR), "students.txt")

cols = [
    "mssv", "ho", "ten", "email", "ngay_sinh", "que_quan",
    "diem_toan", "diem_van", "diem_anh", "diem_tb", "xep_loai"
]

df = pd.read_csv(DATA_PATH, sep="|", header=None, names=cols)

# ======================
# 2. DATA CLEANING
# ======================

# Chuyển điểm sang số
score_cols = ["diem_toan", "diem_van", "diem_anh", "diem_tb"]
for col in score_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Chuẩn hoá quê quán
df["que_quan"] = df["que_quan"].fillna("Unknown")

# Tính lại điểm trung bình
df["diem_tb_clean"] = df[["diem_toan", "diem_van", "diem_anh"]].mean(axis=1)

# ======================
# 3. DATA ANALYSIS + VISUALIZATION
# ======================

# ---- Biểu đồ 1: Tỷ lệ dữ liệu thiếu ----
missing_rate = df[score_cols].isna().mean() * 100
plt.figure()
missing_rate.plot(kind="bar")
plt.title("Tỷ lệ dữ liệu thiếu (%) theo từng cột điểm")
plt.ylabel("% Missing")
plt.show()

# ---- Biểu đồ 2: Phân bố điểm từng môn ----
df[["diem_toan", "diem_van", "diem_anh"]].plot(kind="hist", bins=10)
plt.title("Phân bố điểm Toán - Văn - Anh")
plt.show()

# ---- Biểu đồ 3: So sánh điểm trung bình các môn ----
mean_scores = df[["diem_toan", "diem_van", "diem_anh"]].mean()
plt.figure()
mean_scores.plot(kind="bar")
plt.title("So sánh điểm trung bình các môn")
plt.ylabel("Điểm trung bình")
plt.show()

# ---- Biểu đồ 4: Tiếng Anh vs Toán ----
plt.figure()
plt.scatter(df["diem_toan"], df["diem_anh"])
plt.xlabel("Điểm Toán")
plt.ylabel("Điểm Tiếng Anh")
plt.title("Mối quan hệ giữa điểm Toán và Tiếng Anh")
plt.show()

# ---- Biểu đồ 5: Quê quán vs điểm Tiếng Anh ----
top_locations = (
    df.groupby("que_quan")["diem_anh"]
    .mean()
    .dropna()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure()
top_locations.plot(kind="bar")
plt.title("Top 10 quê quán có điểm Tiếng Anh trung bình cao nhất")
plt.ylabel("Điểm Tiếng Anh")
plt.show()

# ---- Biểu đồ 6: Phân bố xếp loại ----
plt.figure()
df["xep_loai"].value_counts().plot(kind="pie", autopct="%1.1f%%")
plt.title("Tỷ lệ xếp loại học lực")
plt.ylabel("")
plt.show()

# ---- Biểu đồ 7: Boxplot phát hiện ngoại lệ ----
plt.figure()
df[["diem_toan", "diem_van", "diem_anh"]].plot(kind="box")
plt.title("Phát hiện ngoại lệ trong điểm số")
plt.show()
