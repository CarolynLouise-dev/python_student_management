# 🎓 Student Management System

A robust, full-stack application for managing student records, featuring a **FastAPI** backend and a **Pandas-powered** data analysis engine. This system supports full CRUD operations, automated data synthesis, and missing data handling.

## 📌 Key Features

* **Full CRUD Lifecycle:** Add, view, update, and delete student profiles.
* **Data Resiliency:** Support for partial datasets and missing fields.
* **Automated Initialization:** Generates 100 sample student records upon first launch.
* **Advanced Analytics:** Integrated Pandas pipeline for data cleaning and comparative analysis.
* **RESTful API:** Clean JSON-based communication between the frontend and backend.

## 🧱 Tech Stack

### Backend
* **Language:** Python 3.10+
* **Framework:** FastAPI
* **Validation:** Pydantic
* **Analysis:** Pandas
* **Storage:** JSON-based persistence

### Frontend
* **Core:** HTML5 & CSS3
* **Logic:** JavaScript (Fetch API)

---

## 📂 Project Structure

```text
student-management/
├── backend/                # FastAPI application logic
│   ├── main.py             # Entry point & API routes
│   ├── crud.py             # Data handling operations
│   ├── models.py           # Pydantic schemas
│   └── data/               # Persistent storage
├── frontend/               # Web interface
│   ├── index.html
│   ├── css/
│   └── js/
├── docs/                   # Project documentation & reports
└── README.md
```

---

## 🧾 Data Model

The system utilizes a flexible schema where **`mssv`** (Student ID) is the only mandatory unique identifier. All other fields accommodate `null` values to simulate real-world data gaps.

```json
{
  "mssv": "SV1",
  "first_name": "Paul",
  "last_name": "Casey",
  "email": "paul.casey.1@gslingacademy.com",
  "gender": "male",
  "part_time_job": false,
  "absence_days": 3,
  "extracurricular_activities": false,
  "weekly_self_study_hours": 27.0,
  "career_aspiration": "Lawyer",
  "math_score": 73,
  "history_score": 81,
  "physics_score": null,
  "chemistry_score": 97,
  "biology_score": null,
  "english_score": 80,
  "geography_score": 87
}
```

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install fastapi uvicorn pydantic pandas
```

### 2. Launch the Backend
```bash
cd backend
uvicorn main:app --reload
```

### 3. Serve the Frontend
You can open `index.html` directly or serve it via Python:
```bash
cd frontend
python3 -m http.server 5500
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/students` | Retrieve all student records |
| **GET** | `/students/{mssv}` | Retrieve a specific student |
| **POST** | `/students` | Create a new student record |
| **PUT** | `/students/{mssv}` | Update existing student data |
| **DELETE** | `/students/{mssv}` | Remove a student record |

---

## 📊 Data Processing & Analysis

The system leverages **Pandas** to transform raw JSON data into actionable insights:
* **Data Cleaning:** Automated handling of null values and type conversion.
* **Correlation Studies:** Comparing performance metrics (e.g., Math vs. English scores).
* **Demographic Analysis:** Aggregating scores based on hometown or extracurricular involvement.

## 📌 Future Roadmap
* Migration to **PostgreSQL** for scalable data management.
* Frontend migration to **React** or **Vue.js**.
* Dockerization for streamlined deployment.
