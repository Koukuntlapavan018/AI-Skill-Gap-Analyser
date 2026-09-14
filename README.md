# 🤖 AI-Powered Skill Gap Analyzer & Intelligent Career Recommendation System

An AI-powered career guidance application that analyzes a student's resume, identifies their technical skills, compares them with industry job requirements, calculates skill gaps, and recommends suitable career roles and skills to learn.

The application is built using Python and Streamlit and can be accessed through a web browser without installing Python or any additional software.

---

## 🎯 Project Overview

Many students are unsure whether their current technical skills match the requirements of industry job roles.

This project solves this problem by automatically analyzing a student's resume and providing:

- Resume-based skill extraction
- Job-role skill comparison
- Skill match percentage
- Missing skill identification
- Career recommendations
- Skills-to-learn recommendations
- Interactive visual results

---

## ✨ Features

### 📄 Resume Analysis
- Upload a resume in PDF format
- Extract text from digital PDFs
- Perform OCR on scanned/image-based resumes
- Automatically identify technical skills

### 🎯 Skill Gap Analysis
- Compare student skills with job requirements
- Calculate skill match percentage
- Identify matched skills
- Identify missing skills

### 💼 Career Recommendation
- Analyze available job roles
- Calculate compatibility for each role
- Display Top 5 suitable career roles

### 📚 Skills to Learn
- Shows missing skills for the selected job role
- Helps students understand what they should learn next

### 📊 Interactive Dashboard
- Streamlit-based web interface
- Skill match visualization
- Career recommendation chart
- Student profile information
- Job-role analysis

---

## 🧠 System Workflow

```text
                Resume PDF
                    │
                    ▼
            Resume Text Extraction
                    │
          ┌─────────┴─────────┐
          │                   │
     Digital PDF         Scanned PDF
          │                   │
    PyMuPDF Extraction      RapidOCR
          │                   │
          └─────────┬─────────┘
                    ▼
              Skill Detection
                    │
                    ▼
            Student Skill Profile
                    │
                    ▼
          Compare With Job Skills
                    │
                    ▼
             Skill Gap Analysis
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
   Missing Skills       Match Percentage
          │
          ▼
   Skills To Learn
          │
          ▼
   Career Recommendations
          │
          ▼
      Streamlit Dashboard