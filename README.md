# ATTENDRA - AI Powered Attendance System

🔗 **Live Demo:** [Add Streamlit Link Here]

📌 **Demo Access:** Click **Continue as Guest** on the home page to explore the Teacher Dashboard without creating an account.

---

## Overview

ATTENDRA is an AI-powered attendance management system that combines face recognition and voice verification to simplify classroom attendance.

The project was built to explore how machine learning models can be integrated into a complete software application rather than being used only in notebooks and experiments.

The system supports:

* Teacher and Student portals
* Face-based authentication
* AI-assisted attendance marking
* Voice-assisted attendance
* Subject enrollment through QR codes, links, and course codes
* Attendance analytics and history
* Guest demo mode for recruiters and evaluators

---

## Features

### 👨‍🏫 Teacher Portal

* Teacher registration and login
* Create and manage subjects
* View attendance records
* Upload classroom photos for attendance
* Voice-assisted attendance
* Share subjects using:

  * QR Code
  * Direct enrollment link
  * Subject/Course code
* Guest demo mode

---

### 👨‍🎓 Student Portal

* Student registration
* Face-based login
* Enroll into subjects
* View attendance percentage
* View attendance history
* Unenroll from subjects

---

## Attendance Workflow

### Face Attendance Pipeline

1. Teacher uploads classroom photographs.
2. Faces are detected using InsightFace.
3. 512-dimensional face embeddings are generated.
4. Embeddings are matched against enrolled student embeddings.
5. Identified students are added to the attendance queue.

---

### Voice Attendance Pipeline

1. Classroom audio is recorded.
2. Audio is segmented into speech regions.
3. Speaker embeddings are generated using Resemblyzer.
4. Similarity scores are computed against enrolled students.
5. Matched students are added to the attendance queue.

---

## Subject Enrollment

Students can join a subject using three methods:

### 1. QR Code

Teachers can share a generated QR code that automatically opens the enrollment page.

### 2. Direct Enrollment Link

Teachers can share a link that redirects students to the application and pre-fills the subject information.

### 3. Subject Code

Students can manually enter the course code and enroll.

---

## Demo Mode

To allow recruiters and evaluators to explore the application safely, ATTENDRA includes a **Guest Mode**.

Guest Mode provides:

* Demo subjects
* Sample attendance records
* Simulated face and voice attendance
* Safe interaction without modifying production data

---

## Tech Stack

### Frontend

* Streamlit

### Backend & Database

* Supabase
* PostgreSQL
* bcrypt

### Machine Learning & Computer Vision

* InsightFace
* ONNX Runtime
* Resemblyzer
* OpenCV
* NumPy
* Scikit-learn

### Data Processing

* Pandas
* Librosa

### Utilities

* Segno
* Pillow

---

## Project Structure

```text
ATTENDRA
│
├── app.py
├── requirements.txt
├── README.md
└── src
    ├── components
    ├── database
    ├── pipelines
    ├── screens
    └── ui
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/ATTENDRA.git
cd ATTENDRA
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
supabase_url = "YOUR_SUPABASE_URL"
supabase_key = "YOUR_SUPABASE_KEY"
```

Run the application:

```bash
streamlit run app.py
```

---

## Screenshots


* Home Page
* Teacher Dashboard
* Face Attendance
* Attendance Records
* Student Dashboard
* QR Enrollment

---

## What I Learned From Building This Project

This project taught me much more than training machine learning models.

### Robust API Integration & Defensive Programming

I learned to handle missing data, unexpected responses, and validation when integrating with remote databases.

### Understanding Streamlit's Execution Model

I learned how Streamlit's rerun architecture works and how to manage application state using `st.session_state`.

### Separation Between Demo and Production Logic

I implemented a Guest Mode with mocked data, which taught me how to separate business logic from presentation logic.

### Working With Multimodal Data

I learned how to store and process high-dimensional data such as face embeddings and voice embeddings alongside traditional relational data.

### Building User-Centric Interfaces

I learned that good software is not only about functionality but also about user experience, feedback, and responsiveness.

### End-to-End Software Engineering

This project gave me practical experience in combining machine learning, databases, authentication, frontend development, and deployment into one application.

---

## Future Improvements

* Better speaker enrollment and verification
* Attendance analytics dashboard
* Export attendance reports
* Timetable integration
* Email notifications
* Mobile-friendly interface

---

## Author

Built by **Ananya K**

Final Year B.Tech Student | Exploring AI, Machine Learning, and Full-Stack Development
