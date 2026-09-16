import streamlit as st
import pandas as pd
import fitz
import numpy as np
import re

from rapidocr import RapidOCR


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🎯 AI-Powered Skill Gap Analyzer")

st.write(
    """
    Upload your resume and the system will analyze your skills,
    compare them with job requirements, identify skill gaps,
    and recommend suitable career roles.
    """
)


# ============================================================
# LOAD JOB DATA
# ============================================================

@st.cache_data
def load_jobs():

    jobs = pd.read_csv("jobs.csv")

    return jobs


try:

    jobs = load_jobs()

except Exception as e:

    st.error("❌ Could not load jobs.csv")
    st.code(str(e))
    st.stop()


# ============================================================
# SKILLS LIST
# ============================================================

skills_list = [

    "Python",
    "SQL",
    "Excel",
    "Power BI",
    "Statistics",
    "Machine Learning",
    "Deep Learning",
    "Pandas",
    "NumPy",
    "TensorFlow",
    "Scikit-learn",
    "Java",
    "C",
    "C++",
    "DSA",
    "Git",
    "GitHub",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Node.js",
    "Django",
    "Flask",
    "Spring Boot",
    "REST API",
    "NLP",
    "Transformers",
    "PyTorch",
    "ETL",
    "PySpark",
    "AWS",
    "Azure",
    "Linux",
    "Docker",
    "Kubernetes",
    "Jenkins",
    "Networking",
    "Cybersecurity",
    "SIEM",
    "MySQL",
    "PostgreSQL",
    "Database Management",
    "DAX",
    "Data Visualization",
    "Selenium",
    "Software Testing"

]


# ============================================================
# NORMALIZE SKILLS
# ============================================================

def normalize_skill(skill):

    return skill.strip().lower()


# ============================================================
# LOAD RAPIDOCR
# ============================================================

@st.cache_resource
def load_ocr():

    return RapidOCR()


# ============================================================
# EXTRACT TEXT FROM RESUME
# ============================================================

def extract_resume_text(pdf_bytes):

    resume_text = ""

    try:

        pdf = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        total_pages = len(pdf)

        progress = st.progress(0)

        ocr = load_ocr()

        for page_number, page in enumerate(pdf):

            # ------------------------------------------------
            # NORMAL PDF TEXT EXTRACTION
            # ------------------------------------------------

            page_text = page.get_text("text")

            if page_text and page_text.strip():

                resume_text += page_text + "\n"

            else:

                # ------------------------------------------------
                # OCR FOR SCANNED PDF
                # ------------------------------------------------

                pix = page.get_pixmap(
                    matrix=fitz.Matrix(1.5, 1.5),
                    alpha=False
                )

                image = np.frombuffer(
                    pix.samples,
                    dtype=np.uint8
                )

                image = image.reshape(
                    pix.height,
                    pix.width,
                    pix.n
                )

                if pix.n == 4:

                    image = image[:, :, :3]

                # ------------------------------------------------
                # RAPIDOCR
                # ------------------------------------------------

                result = ocr(image)

                if result is not None:

                    detected_text = getattr(
                        result,
                        "txts",
                        None
                    )

                    if detected_text:

                        for text in detected_text:

                            if text:

                                resume_text += (
                                    str(text) + "\n"
                                )

            progress.progress(
                (page_number + 1) / total_pages
            )

        progress.empty()

        pdf.close()

    except Exception as e:

        st.error(
            "❌ Error while reading the resume."
        )

        st.code(str(e))

        return ""

    return resume_text


# ============================================================
# EXTRACT STUDENT NAME
# ============================================================

def extract_name(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    ignored_words = [

        "resume",
        "curriculum vitae",
        "cv",
        "profile",
        "contact",
        "email",
        "phone",
        "mobile",
        "linkedin",
        "github",
        "objective",
        "career objective"

    ]

    for line in lines[:15]:

        lower_line = line.lower()

        if any(
            word in lower_line
            for word in ignored_words
        ):
            continue

        if "@" in line:

            continue

        if re.search(
            r"\d{7,}",
            line
        ):

            continue

        words = line.split()

        if 2 <= len(words) <= 4:

            if all(
                re.match(
                    r"^[A-Za-z.\-]+$",
                    word
                )
                for word in words
            ):

                return line

    return "Not detected"


# ============================================================
# EXTRACT EDUCATION
# ============================================================

def extract_education(text):

    education_patterns = [

        r"\bB\.?\s*Tech\b",
        r"\bB\.?\s*E\b",
        r"\bBCA\b",
        r"\bB\.?\s*Sc\b",
        r"\bM\.?\s*Tech\b",
        r"\bMCA\b",
        r"\bM\.?\s*Sc\b",
        r"\bMBA\b"

    ]

    for pattern in education_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group()

    return "Not detected"


# ============================================================
# EXTRACT GRADUATION YEAR
# ============================================================

def extract_graduation_year(text):

    years = re.findall(
        r"\b20\d{2}\b",
        text
    )

    if years:

        return ", ".join(
            sorted(set(years))
        )

    return "Not detected"


# ============================================================
# DETECT SKILLS
# ============================================================

def detect_skills(text):

    detected = []

    text_lower = text.lower()

    aliases = {

        "js": "JavaScript",
        "javascript": "JavaScript",

        "reactjs": "React",
        "react.js": "React",
        "react": "React",

        "nodejs": "Node.js",
        "node.js": "Node.js",

        "postgres": "PostgreSQL",
        "postgresql": "PostgreSQL",

        "mysql": "MySQL",

        "powerbi": "Power BI",
        "power bi": "Power BI",

        "scikit learn": "Scikit-learn",
        "scikit-learn": "Scikit-learn",

        "sklearn": "Scikit-learn",

        "ml": "Machine Learning",

        "nlp": "NLP",

        "aws": "AWS",

        "gcp": "AWS"

    }

    # --------------------------------------------------------
    # STANDARD SKILL MATCHING
    # --------------------------------------------------------

    for skill in skills_list:

        skill_lower = skill.lower()

        pattern = (
            r"(?<!\w)"
            + re.escape(skill_lower)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            text_lower
        ):

            if skill not in detected:

                detected.append(skill)

    # --------------------------------------------------------
    # ALIAS MATCHING
    # --------------------------------------------------------

    for alias, actual_skill in aliases.items():

        pattern = (
            r"(?<!\w)"
            + re.escape(alias)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            text_lower
        ):

            if actual_skill not in detected:

                detected.append(actual_skill)

    return sorted(detected)


# ============================================================
# CALCULATE JOB MATCH
# ============================================================

def calculate_job_match(
    student_skills,
    required_skills
):

    student_set = set(
        normalize_skill(skill)
        for skill in student_skills
    )

    required_set = set(
        normalize_skill(skill)
        for skill in required_skills
    )

    matched = student_set.intersection(
        required_set
    )

    missing = required_set - student_set

    if len(required_set) == 0:

        percentage = 0

    else:

        percentage = (
            len(matched)
            /
            len(required_set)
        ) * 100

    return (
        matched,
        missing,
        percentage
    )


# ============================================================
# SESSION STATE
# ============================================================

if "analysis_done" not in st.session_state:

    st.session_state.analysis_done = False


if "resume_text" not in st.session_state:

    st.session_state.resume_text = ""


if "student_name" not in st.session_state:

    st.session_state.student_name = ""


if "education" not in st.session_state:

    st.session_state.education = ""


if "graduation_year" not in st.session_state:

    st.session_state.graduation_year = ""


if "student_skills" not in st.session_state:

    st.session_state.student_skills = []


# ============================================================
# FILE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "📄 Upload your resume PDF",
    type=["pdf"]
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

if uploaded_file is not None:

    st.success(
        f"✅ Resume uploaded: {uploaded_file.name}"
    )

    if st.button(
        "🚀 Analyze Resume",
        type="primary"
    ):

        with st.spinner(
            "Analyzing your resume..."
        ):

            pdf_bytes = uploaded_file.read()

            resume_text = extract_resume_text(
                pdf_bytes
            )

        if not resume_text.strip():

            st.error(
                "❌ Could not extract text from this resume."
            )

            st.stop()

        # ----------------------------------------------------
        # SAVE ANALYSIS IN SESSION STATE
        # ----------------------------------------------------

        st.session_state.resume_text = resume_text

        st.session_state.student_name = (
            extract_name(resume_text)
        )

        st.session_state.education = (
            extract_education(resume_text)
        )

        st.session_state.graduation_year = (
            extract_graduation_year(resume_text)
        )

        st.session_state.student_skills = (
            detect_skills(resume_text)
        )

        st.session_state.analysis_done = True


# ============================================================
# DISPLAY ANALYSIS
# ============================================================

if st.session_state.analysis_done:

    student_name = st.session_state.student_name

    education = st.session_state.education

    graduation_year = (
        st.session_state.graduation_year
    )

    student_skills = (
        st.session_state.student_skills
    )


    # ========================================================
    # STUDENT PROFILE
    # ========================================================

    st.header("👨‍🎓 Student Profile")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.subheader("Name")

        st.write(student_name)

    with col2:

        st.subheader("Education")

        st.write(education)

    with col3:

        st.subheader("Graduation Year")

        st.write(graduation_year)


    # ========================================================
    # DETECTED SKILLS
    # ========================================================

    st.header("🛠️ Detected Skills")

    if student_skills:

        st.write(
            ", ".join(student_skills)
        )

    else:

        st.warning(
            "⚠️ No known skills were detected."
        )


    # ========================================================
    # CAREER RECOMMENDATIONS
    # ========================================================

    st.header(
        "💼 Career Recommendations"
    )

    recommendations = []

    for _, job in jobs.iterrows():

        required_skills = [

            skill.strip()

            for skill in str(
                job["required_skills"]
            ).split(",")

        ]

        matched, missing, percentage = (
            calculate_job_match(
                student_skills,
                required_skills
            )
        )

        recommendations.append({

            "Job Role":
                job["job_role"],

            "Match %":
                round(
                    percentage,
                    2
                ),

            "Matched Skills":
                len(matched),

            "Missing Skills":
                len(missing)

        })


    recommendations_df = pd.DataFrame(
        recommendations
    )


    recommendations_df = (
        recommendations_df
        .sort_values(
            "Match %",
            ascending=False
        )
        .reset_index(drop=True)
    )


    # ========================================================
    # TOP 5
    # ========================================================

    top5 = recommendations_df.head(5)

    st.subheader(
        "🏆 Top 5 Suitable Career Roles"
    )

    st.dataframe(
        top5,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # BEST CAREER
    # ========================================================

    best_role = top5.iloc[0]

    st.success(
        f"🎯 Best Match: **{best_role['Job Role']}** "
        f"with **{best_role['Match %']:.2f}%** skill match."
    )


    # ========================================================
    # BAR CHART
    # ========================================================

    st.subheader(
        "📊 Career Match Comparison"
    )

    chart_data = top5.set_index(
        "Job Role"
    )["Match %"]

    st.bar_chart(chart_data)


    # ========================================================
    # DETAILED SKILL GAP ANALYSIS
    # ========================================================

    st.header(
        "🔍 Detailed Skill Gap Analysis"
    )


    # --------------------------------------------------------
    # SELECT JOB ROLE
    # --------------------------------------------------------

    role_list = jobs["job_role"].tolist()

    selected_role = st.selectbox(
        "Choose a job role",
        role_list,
        key="selected_job_role"
    )


    # --------------------------------------------------------
    # GET SELECTED JOB
    # --------------------------------------------------------

    selected_job = jobs[
        jobs["job_role"] == selected_role
    ].iloc[0]


    # --------------------------------------------------------
    # REQUIRED SKILLS
    # --------------------------------------------------------

    required_skills = [

        skill.strip()

        for skill in str(
            selected_job["required_skills"]
        ).split(",")

    ]


    # --------------------------------------------------------
    # CALCULATE SELECTED ROLE GAP
    # --------------------------------------------------------

    matched, missing, percentage = (
        calculate_job_match(
            student_skills,
            required_skills
        )
    )


    # --------------------------------------------------------
    # SELECTED ROLE TITLE
    # --------------------------------------------------------

    st.subheader(
        f"🎯 {selected_role}"
    )


    # --------------------------------------------------------
    # MATCH PERCENTAGE
    # --------------------------------------------------------

    st.metric(
        "Skill Match",
        f"{percentage:.2f}%"
    )


    # ========================================================
    # MATCHED AND MISSING SKILLS
    # ========================================================

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # MATCHED SKILLS
    # --------------------------------------------------------

    with col1:

        st.subheader(
            "✅ Matched Skills"
        )

        if matched:

            st.write(
                ", ".join(
                    sorted(matched)
                )
            )

        else:

            st.write(
                "No matching skills"
            )


    # --------------------------------------------------------
    # MISSING SKILLS
    # --------------------------------------------------------

    with col2:

        st.subheader(
            "❌ Missing Skills"
        )

        if missing:

            st.write(
                ", ".join(
                    sorted(missing)
                )
            )

        else:

            st.write(
                "🎉 No missing skills!"
            )


    # ========================================================
    # SKILLS TO LEARN
    # ========================================================

    st.header(
        "📚 Recommended Skills to Learn"
    )

    if missing:

        for skill in sorted(missing):

            st.write(
                f"➡️ **{skill.title()}**"
            )

    else:

        st.success(
            "🎉 You already have all the required skills for this role!"
        )


    # ========================================================
    # FINAL RECOMMENDATION
    # ========================================================

    st.header(
        "🚀 Career Development Suggestion"
    )


    if missing:

        st.info(
            f"""
            To become more suitable for the **{selected_role}**
            role, focus on learning:

            **{", ".join(sorted(missing))}**

            After learning these skills, build projects and
            add them to your resume to improve your job
            readiness.
            """
        )

    else:

        st.success(
            f"""
            Your current skills match all the listed
            requirements for **{selected_role}**.

            Focus on projects, internships, interview
            preparation and practical experience.
            """
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "AI-Powered Skill Gap Analyzer | "
    "Python • NLP • Machine Learning • Streamlit"
)