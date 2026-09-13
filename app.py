import streamlit as st
import pandas as pd
import fitz


# -----------------------------------
# PAGE SETTINGS
# -----------------------------------

st.set_page_config(
    page_title="AI Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide"
)


# -----------------------------------
# TITLE
# -----------------------------------

st.title("🎯 AI-Powered Skill Gap Analyzer")
st.subheader("Intelligent Career Recommendation System")

st.write(
    "Upload your resume to automatically extract skills, "
    "analyze skill gaps, and receive career recommendations."
)

st.divider()


# -----------------------------------
# LOAD JOB DATASET
# -----------------------------------

jobs = pd.read_csv("jobs.csv")


# -----------------------------------
# SKILL LIST
# -----------------------------------

skills_list = [
    "Python",
    "SQL",
    "Excel",
    "Power BI",
    "Statistics",
    "Machine Learning",
    "Deep Learning",
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
    "NLP",
    "Transformers",
    "PyTorch",
    "ETL",
    "PySpark",
    "AWS",
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
    "REST API",
    "Node.js",
    "Selenium",
    "Software Testing"
]


# -----------------------------------
# RESUME UPLOAD
# -----------------------------------

st.header("📄 Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose your resume PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success("Resume uploaded successfully! ✅")

    # -----------------------------------
    # EXTRACT RESUME TEXT
    # -----------------------------------

    resume_text = ""

    try:

        pdf_document = fitz.open(
            stream=uploaded_file.getvalue(),
            filetype="pdf"
        )

        for page in pdf_document:

            text = page.get_text()

            if text.strip():

                resume_text += text + "\n"

        pdf_document.close()

    except Exception as e:

        st.error(
            f"PDF processing error: {e}"
        )

        st.stop()


    # -----------------------------------
    # CHECK TEXT
    # -----------------------------------

    if not resume_text.strip():

        st.warning(
            "⚠️ This resume appears to be scanned/image-based."
        )

        st.info(
            "The PDF was opened successfully, but it does not "
            "contain selectable text. OCR is required to read "
            "the scanned pages."
        )

        st.stop()


    # -----------------------------------
    # SHOW EXTRACTED TEXT
    # -----------------------------------

    with st.expander(
        "📄 View Extracted Resume Text"
    ):

        st.text_area(
            "Resume Text",
            resume_text,
            height=300
        )


    # -----------------------------------
    # EXTRACT SKILLS
    # -----------------------------------

    st.header("🤖 Extracted Skills")

    resume_lower = resume_text.lower()

    detected_skills = []

    for skill in skills_list:

        if skill.lower() in resume_lower:

            detected_skills.append(skill)


    if detected_skills:

        st.success(
            f"{len(detected_skills)} skills detected! ✅"
        )

        cols = st.columns(4)

        for index, skill in enumerate(
            detected_skills
        ):

            with cols[index % 4]:

                st.info(
                    f"✓ {skill}"
                )

    else:

        st.warning(
            "No matching skills were found."
        )


    # -----------------------------------
    # CAREER RECOMMENDATIONS
    # -----------------------------------

    st.divider()

    st.header(
        "🏆 Top Career Recommendations"
    )

    detected_lower = set(
        skill.lower()
        for skill in detected_skills
    )

    recommendations = []


    for _, job in jobs.iterrows():

        required_skills = [
            skill.strip()
            for skill in job[
                "required_skills"
            ].split(",")
        ]

        required_lower = set(
            skill.lower()
            for skill in required_skills
        )

        matched = detected_lower.intersection(
            required_lower
        )

        if len(required_lower) > 0:

            match_percentage = (
                len(matched)
                / len(required_lower)
            ) * 100

        else:

            match_percentage = 0


        recommendations.append({

            "Job Role": job["job_role"],

            "Match Percentage": round(
                match_percentage,
                2
            ),

            "Matched Skills": len(matched),

            "Required Skills": len(
                required_lower
            )

        })


    # -----------------------------------
    # SORT RECOMMENDATIONS
    # -----------------------------------

    recommendations = sorted(
        recommendations,
        key=lambda x:
        x["Match Percentage"],
        reverse=True
    )


    top_5 = recommendations[:5]


    # -----------------------------------
    # DISPLAY TOP 5
    # -----------------------------------

    for index, recommendation in enumerate(
        top_5,
        1
    ):

        col1, col2 = st.columns(
            [3, 1]
        )

        with col1:

            st.write(
                f"### {index}. "
                f"{recommendation['Job Role']}"
            )

            st.write(
                f"Matched Skills: "
                f"{recommendation['Matched Skills']} / "
                f"{recommendation['Required Skills']}"
            )

        with col2:

            st.metric(
                "Match",
                f"{recommendation['Match Percentage']}%"
            )


    # -----------------------------------
    # CAREER MATCH CHART
    # -----------------------------------

    st.subheader(
        "📊 Career Match Chart"
    )

    chart_data = pd.DataFrame({

        "Career": [
            item["Job Role"]
            for item in top_5
        ],

        "Match Percentage": [
            item["Match Percentage"]
            for item in top_5
        ]

    })

    chart_data = chart_data.set_index(
        "Career"
    )

    st.bar_chart(
        chart_data
    )


    # -----------------------------------
    # TARGET JOB ANALYSIS
    # -----------------------------------

    st.divider()

    st.header(
        "🎯 Target Job Skill Gap"
    )

    job_roles = jobs[
        "job_role"
    ].tolist()


    selected_role = st.selectbox(
        "Select a target job role",
        job_roles
    )


    selected_job = jobs[
        jobs["job_role"] == selected_role
    ].iloc[0]


    required_skills = [

        skill.strip()

        for skill in selected_job[
            "required_skills"
        ].split(",")

    ]


    matched_skills = []

    missing_skills = []


    for skill in required_skills:

        if skill.lower() in detected_lower:

            matched_skills.append(
                skill
            )

        else:

            missing_skills.append(
                skill
            )


    # -----------------------------------
    # TARGET JOB MATCH
    # -----------------------------------

    match_percentage = (

        len(matched_skills)
        / len(required_skills)

    ) * 100


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
            "Missing Skills",
            len(missing_skills)
        )


    # -----------------------------------
    # MATCHED SKILLS
    # -----------------------------------

    st.subheader(
        "✅ Matched Skills"
    )

    if matched_skills:

        st.write(
            ", ".join(matched_skills)
        )

    else:

        st.write(
            "No matched skills."
        )


    # -----------------------------------
    # MISSING SKILLS
    # -----------------------------------

    st.subheader(
        "📚 Skills You Need to Learn"
    )

    if missing_skills:

        for skill in missing_skills:

            st.warning(
                f"Learn: {skill}"
            )

    else:

        st.success(
            "You have all the required skills! 🎉"
        )


# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.caption(
    "AI-Powered Skill Gap Analyzer | "
    "Final Year BTech Project"
)