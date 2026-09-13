import streamlit as st
import pandas as pd
import fitz
import easyocr
import numpy as np
from PIL import Image


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("🎯 AI-Powered Skill Gap Analyzer")
st.write(
    "Upload your resume and analyze your skills, "
    "career matches, and missing skills."
)


# ==========================================
# LOAD JOB DATASET
# ==========================================

jobs = pd.read_csv("jobs.csv")


# ==========================================
# SKILLS LIST
# ==========================================

skills_list = [
    "Python",
    "SQL",
    "Excel",
    "Power BI",
    "Statistics",
    "Machine Learning",
    "TensorFlow",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "Java",
    "DSA",
    "Git",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Django",
    "Flask",
    "Spring Boot",
    "Deep Learning",
    "NLP",
    "ETL",
    "PySpark",
    "AWS",
    "Linux",
    "Docker",
    "Networking",
    "Kubernetes",
    "Jenkins",
    "Cybersecurity",
    "SIEM",
    "MySQL",
    "PostgreSQL",
    "Database Management",
    "DAX",
    "Data Visualization",
    "Node.js",
    "REST API",
    "Transformers",
    "PyTorch",
    "Software Testing",
    "Selenium"
]


# ==========================================
# NORMALIZE SKILL
# ==========================================

def normalize_skill(skill):
    return skill.strip().lower()


# ==========================================
# OCR FUNCTION
# ==========================================

@st.cache_resource
def load_ocr():

    reader = easyocr.Reader(["en"])

    return reader


def extract_resume_text(uploaded_file):

    reader = load_ocr()

    pdf_bytes = uploaded_file.getvalue()

    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    resume_text = ""

    progress = st.progress(0)

    total_pages = len(document)

    for page_number, page in enumerate(document):

        # Render PDF page as image
        pix = page.get_pixmap(
            matrix=fitz.Matrix(2, 2)
        )

        image = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        # Convert image to NumPy
        image_array = np.array(image)

        # OCR
        result = reader.readtext(
            image_array,
            detail=0
        )

        resume_text += "\n".join(result)
        resume_text += "\n"

        progress.progress(
            (page_number + 1) / total_pages
        )

    progress.empty()

    return resume_text


# ==========================================
# UPLOAD RESUME
# ==========================================

uploaded_file = st.file_uploader(
    "📄 Upload your Resume PDF",
    type=["pdf"]
)


if uploaded_file:

    st.success(
        f"Resume uploaded: {uploaded_file.name}"
    )

    # ======================================
    # EXTRACT TEXT
    # ======================================

    with st.spinner("🔍 Reading your resume..."):

        resume_text = extract_resume_text(
            uploaded_file
        )


    # ======================================
    # SHOW RESUME TEXT
    # ======================================

    st.subheader("📄 Extracted Resume Text")

    if resume_text.strip():

        st.text_area(
            "Resume Content",
            resume_text,
            height=250
        )

    else:

        st.error(
            "❌ Could not extract text from the resume."
        )

        st.stop()


    # ======================================
    # SKILL DETECTION
    # ======================================

    st.subheader("🧠 Skills Detected")

    resume_lower = resume_text.lower()

    detected_skills = []

    for skill in skills_list:

        if skill.lower() in resume_lower:

            detected_skills.append(skill)


    if detected_skills:

        st.success(
            f"Detected {len(detected_skills)} skills"
        )

        st.write(
            ", ".join(detected_skills)
        )

    else:

        st.warning(
            "No known skills detected."
        )


    # ======================================
    # CAREER RECOMMENDATIONS
    # ======================================

    st.subheader("🚀 Career Recommendations")


    student_skills = set(
        normalize_skill(skill)
        for skill in detected_skills
    )


    recommendations = []


    for _, job in jobs.iterrows():

        job_skills = set(
            normalize_skill(skill)
            for skill in job["required_skills"].split(",")
        )

        matched = student_skills.intersection(
            job_skills
        )

        percentage = (
            len(matched) / len(job_skills)
        ) * 100

        recommendations.append(
            (
                job["job_role"],
                percentage
            )
        )


    # Sort
    recommendations.sort(
        key=lambda x: x[1],
        reverse=True
    )


    # ======================================
    # TOP 5
    # ======================================

    top5 = recommendations[:5]


    for rank, (role, percentage) in enumerate(
        top5,
        1
    ):

        st.write(
            f"**{rank}. {role} — "
            f"{percentage:.2f}% match**"
        )


    # ======================================
    # CHART
    # ======================================

    chart_data = pd.DataFrame(
        top5,
        columns=[
            "Job Role",
            "Match Percentage"
        ]
    )

    chart_data = chart_data.set_index(
        "Job Role"
    )

    st.bar_chart(
        chart_data
    )


    # ======================================
    # TARGET JOB
    # ======================================

    st.subheader("🎯 Skill Gap Analysis")


    selected_role = st.selectbox(
        "Select a job role",
        jobs["job_role"]
    )


    selected_job = jobs[
        jobs["job_role"] == selected_role
    ].iloc[0]


    required_skills = set(
        normalize_skill(skill)
        for skill in selected_job[
            "required_skills"
        ].split(",")
    )


    matched_skills = (
        student_skills.intersection(
            required_skills
        )
    )


    missing_skills = (
        required_skills - student_skills
    )


    match_percentage = (
        len(matched_skills)
        / len(required_skills)
    ) * 100


    # ======================================
    # RESULTS
    # ======================================

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Skill Match",
            f"{match_percentage:.2f}%"
        )


    with col2:

        st.metric(
            "Matched Skills",
            len(matched_skills)
        )


    with col3:

        st.metric(
            "Missing Skills",
            len(missing_skills)
        )


    # ======================================
    # MATCHED SKILLS
    # ======================================

    st.write("### ✅ Your Skills")

    if matched_skills:

        st.write(
            ", ".join(
                sorted(matched_skills)
            )
        )

    else:

        st.write("None")


    # ======================================
    # MISSING SKILLS
    # ======================================

    st.write("### ❌ Skills You Need to Learn")

    if missing_skills:

        st.warning(
            ", ".join(
                sorted(missing_skills)
            )
        )

    else:

        st.success(
            "🎉 You have all required skills!"
        )


    # ======================================
    # FINAL MESSAGE
    # ======================================

    st.success(
        "✅ Skill Gap Analysis Completed!"
    )