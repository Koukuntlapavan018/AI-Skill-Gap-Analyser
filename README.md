# 🎯 AI-Powered Skill Gap Analyzer & Intelligent Career Recommendation System

An AI-powered resume analysis and career recommendation system that analyzes a student's resume, detects technical skills, compares them with job requirements, identifies skill gaps, recommends suitable career roles, and generates a personalized learning roadmap.

---

## 📌 Project Overview

Students often find it difficult to understand:

- Which technical skills they currently have
- Which skills are required for a particular career
- Which skills they are missing
- Which career roles match their current profile
- What they should learn next

This project provides an intelligent solution by analyzing a resume and comparing the extracted skills with predefined job-role requirements.

The system also generates a **Personalized Learning Roadmap** based on the selected career role and missing skills.

---

## 🚀 Key Features

### 📄 1. Resume Upload

Users can upload their resume in PDF format.

The system supports:

- Text-based PDF resumes
- Scanned/image-based PDF resumes
- OCR-based text extraction

---

### 🔍 2. Resume Text Extraction

The application extracts text from uploaded resumes using:

- PyMuPDF
- RapidOCR

If normal PDF text extraction fails, the system automatically uses OCR for scanned pages.

---

### 👨‍🎓 3. Student Profile Extraction

The system attempts to identify:

- Student Name
- Education
- Graduation Year
- Technical Skills

---

### 🧠 4. Automatic Skill Detection

The system detects technical skills from the resume.

Examples include:

- Python
- SQL
- Excel
- Power BI
- Machine Learning
- Deep Learning
- Pandas
- NumPy
- Java
- DSA
- Git
- GitHub
- HTML
- CSS
- JavaScript
- React
- Django
- Flask
- AWS
- Docker
- Linux
- NLP
- PyTorch
- TensorFlow
- Selenium
- Software Testing

---

### 💼 5. Career Recommendation

The system compares the student's detected skills with job-role requirements.

It calculates:

```text
Skill Match Percentage =
(Matched Skills / Required Skills) × 100