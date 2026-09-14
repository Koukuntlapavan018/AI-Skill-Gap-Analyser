import streamlit as st
import pandas as pd
import fitz
import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
import re


# ==========================================
# PAGE CONFIG
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
    "Upload your resume to analyze your skills, "
    "find suitable job roles, and identify skill gaps."
)


# ==========================================
# LOAD JOB DATA
# ==========================================

jobs = pd.read_csv("jobs.csv")


# ==========================================
# SKILL DATABASE
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
# NORMALIZE
# ==========================================

def normalize_skill(skill):
    return skill.strip().lower()


# ==========================================
# LOAD OCR ONCE
# ==========================================

@st.cache_resource
def load_ocr():

    return RapidOCR()


# ==========================================
# EXTRACT TEXT FROM PDF
# ==========================================

def extract_resume_text(uploaded_file):

    pdf_bytes = uploaded_file.getvalue()

    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    resume_text = ""

    ocr = load_ocr()

    progress = st.progress(0)

    total_pages = len(document)

    for page_number, page in enumerate(document):

        # ----------------------------------
        # FIRST TRY NORMAL PDF TEXT
        # ----------------------------------

        page_text = page.get_text("text")

        if page_text.strip():

            resume_text += page_text
            resume_text += "\n"

        else:

            # ----------------------------------
            # SCANNED PDF → OCR
            # ----------------------------------

            pix = page.get_pixmap(
                matrix=fitz.Matrix(1.5, 1.5),
                alpha=False
            )

            image = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            image_array = np.array(image)

            result, _ = ocr(image_array)

            if result:

                for item in result:

                    if len(item) >= 2:

                        detected_text = item[1]

                        resume_text += (
                            str(detected_text)
                            + "\n"
                        )

        progress.progress(
            (page_number + 1) / total_pages
        )

    progress.empty()

    document.close()

    return resume_text


# ==========================================
# STUDENT NAME
# ==========================================

def extract_student_name(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    ignore_words = [
        "resume",
        "curriculum",
        "vitae",
        "email",
        "phone",
        "mobile",
        "contact",
        "linkedin",
        "github",
        "objective",
        "profile",
        "education",
        "skills"
    ]

    for line in lines[:12]:

        clean_line = re.sub(
            r"[^A-Za-z .]",
            "",
            line
        ).strip()

        words = clean_line.split()

        if 2 <= len(words) <= 5:

            lower_line = clean_line.lower()

            if not any(
                word in lower_line
                for word in ignore_words
            ):

                return clean_line

    return "Student"


# ==========================================
# EDUCATION
# ==========================================

def extract_education(text):

    text_lower = text.lower()

    if (
        "b.tech" in text_lower
        or "btech" in text_lower
        or "bachelor of technology" in text_lower
    ):
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
# GRADUATION YEAR
# ==========================================

def extract_graduation_year(text):

    years = re.findall(
        r"\b20\d{2}\b",
        text
    )

    years = [
        int(year)
        for year in years
    ]

    valid_years = [
        year
        for year in years
        if 2024 <= year <= 2035
    ]

    if valid_years:

        return str(max(valid_years))

    return "Not detected"


# ==========================================
# DETECT SKILLS
# ==========================================

def detect_skills(text):

    text_lower = text.lower()

    detected = []

    for skill in skills_list:

        # Escape special characters
        pattern = re.escape(
            skill.lower()
        )

        # Whole-word style matching
        if re.search(
            r"(?<!\w)"
            + pattern
            + r"(?!\w)",
            text_lower
        ):

            detected.append(skill)

    return detected


# ==========================================
# MAIN APP
# ==========================================

uploaded_file = st.file_uploader(
    "📄 Upload Resume PDF",
    type=["pdf"]
)


if uploaded_file:

    st.success(
        f"Resume uploaded: {uploaded_file.name}"
    )

    # --------------------------------------
    # RESUME PROCESSING
    # --------------------------------------

    with st.spinner(
        "🔍 Analyzing resume..."
    ):

        resume_text = extract_resume_text(
            uploaded_file
        )

    if not resume_text.strip():

        st.error(
            "❌ No readable text was found "
            "in this resume."
        )

        st.stop()


    # --------------------------------------
    # STUDENT PROFILE
    # --------------------------------------

    student_name = extract_student_name(
        resume_text
    )

    education = extract_education(
        resume_text
    )

    graduation_year = extract_graduation_year(
        resume_text
    )

    detected_skills = detect_skills(
        resume_text
    )

    student_skills = set(
        normalize_skill(skill)
        for skill in detected_skills
    )


    st.header("👤 Student Profile")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown("**👨‍🎓 Name**")

        st.write(student_name)


    with col2:

        st.markdown("**🎓 Education**")

        st.write(education)


    with col3:

        st.markdown("**📅 Graduation**")

        st.write(graduation_year)


    # --------------------------------------
    # SKILLS
    # --------------------------------------

    st.header("🧠 Skills Identified")


    if detected_skills:

        st.success(
            " • ".join(
                sorted(detected_skills)
            )
        )

    else:

        st.warning(
            "No known technical skills detected."
        )


    # --------------------------------------
    # JOB RECOMMENDATIONS
    # --------------------------------------

    st.header(
        "💼 Recommended Job Roles"
    )


    recommendations = []


    for _, job in jobs.iterrows():

        job_skills = set(
            normalize_skill(skill)
            for skill in
            job["required_skills"].split(",")
        )

        matched = (
            student_skills
            .intersection(job_skills)
        )

        percentage = (
            len(matched)
            / len(job_skills)
        ) * 100

        recommendations.append({

            "Job Role": job["job_role"],

            "Match Percentage": percentage,

            "Matched": len(matched),

            "Total": len(job_skills)

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


    # --------------------------------------
    # BEST ROLE
    # --------------------------------------

    best_role = recommendations_df.iloc[0]


    st.success(
        f"🏆 Best Match: "
        f"{best_role['Job Role']} — "
        f"{best_role['Match Percentage']:.1f}%"
    )


    # --------------------------------------
    # TOP 5
    # --------------------------------------

    top5 = recommendations_df.head(5)


    st.dataframe(
        top5[
            [
                "Job Role",
                "Match Percentage",
                "Matched",
                "Total"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------
    # CHART
    # --------------------------------------

    chart_data = top5[
        [
            "Job Role",
            "Match Percentage"
        ]
    ].set_index(
        "Job Role"
    )


    st.bar_chart(chart_data)


    # --------------------------------------
    # SKILL GAP
    # --------------------------------------

    st.header(
        "🎯 Skill Gap Analysis"
    )


    selected_role = st.selectbox(
        "Select a target job role",
        jobs["job_role"].tolist()
    )


    selected_job = jobs[
        jobs["job_role"]
        == selected_role
    ].iloc[0]


    required_skills = set(
        normalize_skill(skill)
        for skill in
        selected_job[
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


    # --------------------------------------
    # METRICS
    # --------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Skill Match",
            f"{match_percentage:.1f}%"
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


    # --------------------------------------
    # MATCHED
    # --------------------------------------

    st.subheader(
        "✅ Skills You Have"
    )


    if matched_skills:

        st.write(
            " • ".join(
                sorted(matched_skills)
            )
        )

    else:

        st.write("None")


    # --------------------------------------
    # MISSING
    # --------------------------------------

    st.subheader(
        "📚 Skills to Learn"
    )


    if missing_skills:

        for skill in sorted(
            missing_skills
        ):

            st.write(
                f"📌 {skill.title()}"
            )

    else:

        st.success(
            "🎉 You already have all "
            "required skills!"
        )


    # --------------------------------------
    # FINAL MESSAGE
    # --------------------------------------

    if match_percentage >= 80:

        st.success(
            f"You are highly prepared for "
            f"{selected_role}."
        )

    elif match_percentage >= 50:

        st.warning(
            f"You have a good foundation for "
            f"{selected_role}. "
            f"Learn the missing skills."
        )

    else:

        st.info(
            f"You need more preparation for "
            f"{selected_role}. "
            f"Focus on the recommended skills."
        )


    st.success(
        "✅ Analysis completed successfully!"
    )