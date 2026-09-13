import streamlit as st
import pandas as pd
import fitz
import easyocr
import numpy as np
from PIL import Image
import re


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
    "Analyze a student's resume, identify skills, "
    "recommend suitable job roles, and find skill gaps."
)


# ==========================================
# LOAD JOB DATA
# ==========================================

jobs = pd.read_csv("jobs.csv")


# ==========================================
# SKILLS DATABASE
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
# OCR MODEL
# ==========================================

@st.cache_resource
def load_ocr():

    reader = easyocr.Reader(["en"])

    return reader


# ==========================================
# EXTRACT TEXT FROM RESUME
# ==========================================

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

        pix = page.get_pixmap(
            matrix=fitz.Matrix(2, 2)
        )

        image = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        image_array = np.array(image)

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
# EXTRACT STUDENT NAME
# ==========================================

def extract_student_name(text):

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    # Try lines containing name
    for line in lines[:10]:

        clean_line = re.sub(
            r"[^A-Za-z .]",
            "",
            line
        ).strip()

        words = clean_line.split()

        if (
            2 <= len(words) <= 5
            and not any(
                keyword in clean_line.lower()
                for keyword in [
                    "resume",
                    "curriculum",
                    "vitae",
                    "email",
                    "phone",
                    "contact",
                    "linkedin",
                    "github"
                ]
            )
        ):

            return clean_line

    return "Student"


# ==========================================
# EXTRACT EDUCATION
# ==========================================

def extract_education(text):

    text_lower = text.lower()

    if "b.tech" in text_lower or "btech" in text_lower:

        return "B.Tech"

    if "bachelor of technology" in text_lower:

        return "B.Tech"

    if "b.e" in text_lower:

        return "B.E"

    if "bca" in text_lower:

        return "BCA"

    if "b.sc" in text_lower:

        return "B.Sc"

    if "m.tech" in text_lower:

        return "M.Tech"

    if "mca" in text_lower:

        return "MCA"

    return "Not detected"


# ==========================================
# EXTRACT GRADUATION YEAR
# ==========================================

def extract_graduation_year(text):

    matches = re.findall(
        r"\b20\d{2}\b",
        text
    )

    years = [
        int(year)
        for year in matches
    ]

    # Prefer future/latest academic year
    valid_years = [
        year
        for year in years
        if 2024 <= year <= 2035
    ]

    if valid_years:

        return str(max(valid_years))

    return "Not detected"


# ==========================================
# UPLOAD RESUME
# ==========================================

uploaded_file = st.file_uploader(
    "📄 Upload Student Resume",
    type=["pdf"]
)


if uploaded_file:

    st.success(
        f"✅ Resume uploaded: {uploaded_file.name}"
    )


    # ======================================
    # OCR
    # ======================================

    with st.spinner(
        "🔍 AI is analyzing the resume..."
    ):

        resume_text = extract_resume_text(
            uploaded_file
        )


    if not resume_text.strip():

        st.error(
            "❌ Could not extract information "
            "from this resume."
        )

        st.stop()


    # ======================================
    # STUDENT PROFILE
    # ======================================

    student_name = extract_student_name(
        resume_text
    )

    education = extract_education(
        resume_text
    )

    graduation_year = extract_graduation_year(
        resume_text
    )


    # ======================================
    # DETECT SKILLS
    # ======================================

    resume_lower = resume_text.lower()

    detected_skills = []

    for skill in skills_list:

        if skill.lower() in resume_lower:

            detected_skills.append(skill)


    student_skills = set(
        normalize_skill(skill)
        for skill in detected_skills
    )


    # ======================================
    # STUDENT PROFILE DISPLAY
    # ======================================

    st.subheader("👤 Student Profile")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown("### 👨‍🎓 Name")

        st.write(student_name)


    with col2:

        st.markdown("### 🎓 Education")

        st.write(education)


    with col3:

        st.markdown("### 📅 Graduation")

        st.write(graduation_year)


    # ======================================
    # SKILLS
    # ======================================

    st.subheader("🧠 Skills Identified")


    if detected_skills:

        skill_text = " • ".join(
            sorted(detected_skills)
        )

        st.info(skill_text)

    else:

        st.warning(
            "No known technical skills detected."
        )


    # ======================================
    # JOB ROLE RECOMMENDATIONS
    # ======================================

    st.subheader(
        "💼 Recommended Job Roles"
    )


    recommendations = []


    for _, job in jobs.iterrows():

        job_skills = set(
            normalize_skill(skill)
            for skill in job[
                "required_skills"
            ].split(",")
        )

        matched = (
            student_skills.intersection(
                job_skills
            )
        )

        percentage = (
            len(matched)
            / len(job_skills)
        ) * 100


        recommendations.append({

            "Job Role": job["job_role"],

            "Match Percentage": percentage,

            "Matched Skills": len(matched),

            "Total Skills": len(job_skills)

        })


    recommendations_df = pd.DataFrame(
        recommendations
    )


    recommendations_df = (
        recommendations_df
        .sort_values(
            "Match Percentage",
            ascending=False
        )
        .reset_index(drop=True)
    )


    # ======================================
    # BEST MATCH
    # ======================================

    best_role = recommendations_df.iloc[0]


    st.success(
        f"🏆 Best Career Match: "
        f"{best_role['Job Role']} "
        f"({best_role['Match Percentage']:.2f}%)"
    )


    # ======================================
    # TOP 5 JOBS
    # ======================================

    top5 = recommendations_df.head(5)


    for index, row in top5.iterrows():

        rank = index + 1

        st.write(
            f"**{rank}. {row['Job Role']}**"
        )

        st.progress(
            int(row["Match Percentage"])
        )

        st.caption(
            f"{row['Match Percentage']:.2f}% match"
        )


    # ======================================
    # CHART
    # ======================================

    st.subheader(
        "📊 Career Match Comparison"
    )


    chart_data = top5[
        [
            "Job Role",
            "Match Percentage"
        ]
    ].set_index(
        "Job Role"
    )


    st.bar_chart(
        chart_data
    )


    # ======================================
    # TARGET JOB
    # ======================================

    st.subheader(
        "🎯 Skill Gap Analysis"
    )


    selected_role = st.selectbox(
        "Choose a target job role",
        jobs["job_role"].tolist()
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
        student_skills
        .intersection(required_skills)
    )


    missing_skills = (
        required_skills
        - student_skills
    )


    match_percentage = (
        len(matched_skills)
        / len(required_skills)
    ) * 100


    # ======================================
    # SKILL GAP METRICS
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
            "Skills to Learn",
            len(missing_skills)
        )


    # ======================================
    # MATCHED SKILLS
    # ======================================

    st.write(
        "### ✅ Skills You Already Have"
    )


    if matched_skills:

        st.success(
            " • ".join(
                sorted(matched_skills)
            )
        )

    else:

        st.write(
            "No matching skills found."
        )


    # ======================================
    # MISSING SKILLS
    # ======================================

    st.write(
        "### 📚 Recommended Skills to Learn"
    )


    if missing_skills:

        for skill in sorted(missing_skills):

            st.write(
                f"📌 **{skill.title()}**"
            )

    else:

        st.success(
            "🎉 You have all the required skills!"
        )


    # ======================================
    # FINAL RECOMMENDATION
    # ======================================

    st.subheader(
        "🚀 Career Development Suggestion"
    )


    if match_percentage >= 80:

        st.success(
            f"You are highly suitable for "
            f"**{selected_role}**. "
            f"Focus on strengthening your existing skills."
        )

    elif match_percentage >= 50:

        st.warning(
            f"You have a good foundation for "
            f"**{selected_role}**. "
            f"Learn the missing skills to improve your chances."
        )

    else:

        st.info(
            f"You need additional preparation for "
            f"**{selected_role}**. "
            f"Start by learning the recommended skills."
        )


    # ======================================
    # COMPLETED
    # ======================================

    st.success(
        "✅ AI Skill Gap Analysis Completed!"
    )