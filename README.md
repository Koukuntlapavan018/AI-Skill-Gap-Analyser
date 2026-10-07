# 🎯 AI-Powered Skill Gap Analyzer & Intelligent Career Recommendation System

An AI-powered web application that analyzes a student's resume, identifies their technical skills, compares them with job-role requirements, calculates skill gaps, recommends suitable career roles, and generates a personalized learning roadmap.

The system uses **Python, NLP, OCR, Machine Learning concepts, Pandas, Streamlit and data-driven skill matching** to help students understand their career readiness.

---

## 🚀 Live Demo

🌐 **Streamlit Application:**

https://ai-skill-gap-analyser-j4tykkqfcwh58qvlmcou6.streamlit.app

Users can upload their resume and receive:

- 👤 Student profile extraction
- 🧠 Automatic skill detection
- 💼 Career recommendations
- 📊 Skill-match percentage
- ❌ Missing skill identification
- 📚 Personalized learning roadmap
- 🎯 Career development suggestions

---

## 📌 Project Overview

Students often find it difficult to understand:

- Which skills they already have
- Which skills are required for a particular job
- What skills they are missing
- Which career roles match their current profile
- What they should learn next

This project addresses these problems by automatically analyzing a student's resume and comparing the extracted skills with predefined job-role requirements.

The system converts resume information into a structured **student skill profile** and performs skill-gap analysis against multiple career roles.

---

# 🧠 How the System Works

```text
                    Resume PDF
                        │
                        ▼
                Resume Processing
                        │
                        ▼
                 Text Extraction
                        │
              ┌─────────┴─────────┐
              │                   │
        Digital Resume       Scanned Resume
              │                   │
          PyMuPDF               OCR
              │              RapidOCR
              └─────────┬─────────┘
                        │
                        ▼
                 Skill Detection
                        │
                        ▼
              Student Skill Profile
                        │
                        ▼
              Job Requirement Data
                        │
                        ▼
              Skill Matching Engine
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
        Matched Skills       Missing Skills
              │                   │
              └─────────┬─────────┘
                        ▼
                Skill Gap Analysis
                        │
                        ▼
              Career Recommendations
                        │
                        ▼
           Personalized Learning Roadmap
           