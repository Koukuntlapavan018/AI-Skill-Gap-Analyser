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
# HEADER
# ============================================================

st.title("🎯 AI-Powered Skill Gap Analyzer")
st.subheader("Intelligent Career Recommendation System")

st.write(
    """
Upload your resume to analyze your skills, identify suitable
career roles, find skill gaps, and generate a personalized
learning roadmap.
"""
)


# ============================================================
# LOAD JOB DATA
# ============================================================

@st.cache_data
def load_jobs():

    return pd.read_csv("jobs.csv")


jobs = load_jobs()


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
# PERSONALIZED LEARNING ROADMAP
# ============================================================

learning_roadmap = {

    "python": {
        "phase": "Programming Fundamentals",
        "duration": "2 weeks",
        "topics": [
            "Python syntax",
            "Variables and data types",
            "Conditions and loops",
            "Functions",
            "Lists, tuples, sets and dictionaries",
            "File handling",
            "Object-oriented programming"
        ],
        "project": "Build a Python Student Management System"
    },

    "sql": {
        "phase": "Database Fundamentals",
        "duration": "1 week",
        "topics": [
            "SELECT queries",
            "WHERE conditions",
            "ORDER BY",
            "GROUP BY",
            "Aggregate functions",
            "JOIN operations",
            "Subqueries",
            "Window functions"
        ],
        "project": "Build a SQL Sales Analysis Database"
    },

    "excel": {
        "phase": "Data Analysis",
        "duration": "5 days",
        "topics": [
            "Excel formulas",
            "Functions",
            "Sorting and filtering",
            "Pivot tables",
            "Charts",
            "Lookup functions",
            "Data cleaning"
        ],
        "project": "Create an Excel Sales Dashboard"
    },

    "power bi": {
        "phase": "Business Intelligence",
        "duration": "1 week",
        "topics": [
            "Power BI interface",
            "Importing datasets",
            "Data cleaning",
            "Power Query",
            "Relationships",
            "Visualizations",
            "Dashboard creation"
        ],
        "project": "Build an Interactive Business Dashboard"
    },

    "statistics": {
        "phase": "Statistics",
        "duration": "1 week",
        "topics": [
            "Mean, median and mode",
            "Variance and standard deviation",
            "Probability",
            "Correlation",
            "Regression basics",
            "Hypothesis testing"
        ],
        "project": "Perform Statistical Analysis on a Dataset"
    },

    "machine learning": {
        "phase": "Machine Learning",
        "duration": "2 weeks",
        "topics": [
            "Machine learning fundamentals",
            "Supervised learning",
            "Unsupervised learning",
            "Linear regression",
            "Logistic regression",
            "Decision trees",
            "Model evaluation"
        ],
        "project": "Build a Student Performance Prediction Model"
    },

    "deep learning": {
        "phase": "Deep Learning",
        "duration": "2 weeks",
        "topics": [
            "Neural networks",
            "Activation functions",
            "Forward propagation",
            "Backpropagation",
            "CNN",
            "RNN basics",
            "Model training"
        ],
        "project": "Build an Image Classification Model"
    },

    "pandas": {
        "phase": "Data Manipulation",
        "duration": "4 days",
        "topics": [
            "Series and DataFrames",
            "Reading CSV files",
            "Filtering data",
            "Sorting data",
            "Missing values",
            "GroupBy",
            "Data transformation"
        ],
        "project": "Analyze a Real-World CSV Dataset"
    },

    "numpy": {
        "phase": "Numerical Computing",
        "duration": "3 days",
        "topics": [
            "NumPy arrays",
            "Array operations",
            "Indexing",
            "Slicing",
            "Mathematical operations",
            "Matrix operations"
        ],
        "project": "Build a Numerical Data Analysis Program"
    },

    "tensorflow": {
        "phase": "Deep Learning Framework",
        "duration": "1 week",
        "topics": [
            "TensorFlow basics",
            "Keras",
            "Creating neural networks",
            "Training models",
            "Evaluation",
            "Prediction"
        ],
        "project": "Build a TensorFlow Classification Model"
    },

    "scikit-learn": {
        "phase": "Machine Learning Tools",
        "duration": "1 week",
        "topics": [
            "Dataset preparation",
            "Train-test split",
            "Preprocessing",
            "Classification",
            "Regression",
            "Clustering",
            "Model evaluation"
        ],
        "project": "Build an ML Prediction System"
    },

    "java": {
        "phase": "Java Programming",
        "duration": "2 weeks",
        "topics": [
            "Java syntax",
            "Variables",
            "Conditions and loops",
            "Methods",
            "Arrays",
            "OOP concepts",
            "Exception handling"
        ],
        "project": "Build a Java Banking Application"
    },

    "c": {
        "phase": "Programming Fundamentals",
        "duration": "1 week",
        "topics": [
            "C syntax",
            "Variables",
            "Conditions",
            "Loops",
            "Functions",
            "Arrays",
            "Pointers"
        ],
        "project": "Build a C Student Management System"
    },

    "c++": {
        "phase": "C++ Programming",
        "duration": "1 week",
        "topics": [
            "C++ syntax",
            "Functions",
            "Classes",
            "Objects",
            "Inheritance",
            "Polymorphism",
            "STL"
        ],
        "project": "Build a C++ Inventory System"
    },

    "dsa": {
        "phase": "Problem Solving",
        "duration": "3 weeks",
        "topics": [
            "Arrays",
            "Strings",
            "Linked lists",
            "Stacks",
            "Queues",
            "Trees",
            "Graphs",
            "Sorting and searching"
        ],
        "project": "Solve 50 DSA Coding Problems"
    },

    "git": {
        "phase": "Developer Tools",
        "duration": "2 days",
        "topics": [
            "Git basics",
            "Repositories",
            "Commits",
            "Branches",
            "Merging",
            "Git workflow",
            "Remote repositories"
        ],
        "project": "Create and Manage a Git Project"
    },

    "github": {
        "phase": "Developer Portfolio",
        "duration": "2 days",
        "topics": [
            "GitHub repositories",
            "README files",
            "GitHub branches",
            "Pull requests",
            "Issues",
            "Project documentation"
        ],
        "project": "Create a Professional GitHub Portfolio"
    },

    "html": {
        "phase": "Web Fundamentals",
        "duration": "3 days",
        "topics": [
            "HTML structure",
            "Headings",
            "Forms",
            "Tables",
            "Links",
            "Images",
            "Semantic HTML"
        ],
        "project": "Build a Personal Portfolio Website"
    },

    "css": {
        "phase": "Web Design",
        "duration": "4 days",
        "topics": [
            "Selectors",
            "Colors",
            "Box model",
            "Flexbox",
            "Grid",
            "Responsive design",
            "Animations"
        ],
        "project": "Design a Responsive Portfolio Website"
    },

    "javascript": {
        "phase": "Web Programming",
        "duration": "1 week",
        "topics": [
            "JavaScript syntax",
            "Variables",
            "Functions",
            "Arrays",
            "Objects",
            "DOM manipulation",
            "Events"
        ],
        "project": "Build an Interactive Web Application"
    },

    "react": {
        "phase": "Frontend Development",
        "duration": "2 weeks",
        "topics": [
            "React components",
            "Props",
            "State",
            "Hooks",
            "Events",
            "Forms",
            "API integration"
        ],
        "project": "Build a React Dashboard"
    },

    "node.js": {
        "phase": "Backend Development",
        "duration": "1 week",
        "topics": [
            "Node.js basics",
            "Modules",
            "NPM",
            "Express",
            "Routes",
            "Middleware",
            "REST APIs"
        ],
        "project": "Build a Node.js REST API"
    },

    "django": {
        "phase": "Python Web Development",
        "duration": "2 weeks",
        "topics": [
            "Django basics",
            "Projects and apps",
            "Models",
            "Views",
            "Templates",
            "Forms",
            "Database integration"
        ],
        "project": "Build a Django Job Portal"
    },

    "flask": {
        "phase": "Python Backend",
        "duration": "1 week",
        "topics": [
            "Flask basics",
            "Routes",
            "Templates",
            "Forms",
            "APIs",
            "Database connection"
        ],
        "project": "Build a Flask REST API"
    },

    "spring boot": {
        "phase": "Java Backend",
        "duration": "2 weeks",
        "topics": [
            "Spring Boot basics",
            "Controllers",
            "Services",
            "Repositories",
            "REST APIs",
            "Database integration"
        ],
        "project": "Build a Spring Boot Backend"
    },

    "rest api": {
        "phase": "API Development",
        "duration": "4 days",
        "topics": [
            "HTTP methods",
            "GET and POST",
            "PUT and DELETE",
            "JSON",
            "API authentication",
            "API testing"
        ],
        "project": "Build a REST API for a Student System"
    }
}
# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_skill(skill):
    return skill.strip().lower()


# ============================================================
# OCR MODEL
# ============================================================

@st.cache_resource
def load_ocr():

    return RapidOCR()


# ============================================================
# RESUME TEXT EXTRACTION
# ============================================================

def extract_resume_text(pdf_bytes):

    resume_text = ""

    try:

        doc = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        ocr = load_ocr()

        progress = st.progress(0)

        total_pages = len(doc)

        for page_number, page in enumerate(doc):

            # ------------------------------------------------
            # First try normal PDF text extraction
            # ------------------------------------------------

            page_text = page.get_text("text")

            if page_text and page_text.strip():

                resume_text += (
                    page_text.strip()
                    + "\n"
                )

            else:

                # --------------------------------------------
                # OCR for scanned/image-based pages
                # --------------------------------------------

                pix = page.get_pixmap(
                    matrix=fitz.Matrix(1.5, 1.5),
                    alpha=False
                )

                img = np.frombuffer(
                    pix.samples,
                    dtype=np.uint8
                )

                img = img.reshape(
                    pix.height,
                    pix.width,
                    pix.n
                )

                if pix.n == 4:

                    img = img[:, :, :3]

                result = ocr(img)

                if result and result.txts:

                    page_ocr_text = "\n".join(
                        result.txts
                    )

                    resume_text += (
                        page_ocr_text
                        + "\n"
                    )

            progress.progress(
                (page_number + 1) / total_pages
            )

        doc.close()

        progress.empty()

    except Exception as e:

        st.error(
            f"Resume processing error: {e}"
        )

    return resume_text


# ============================================================
# NAME EXTRACTION
# ============================================================

def extract_name(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines[:15]:

        lower_line = line.lower()

        if any(
            word in lower_line
            for word in [
                "resume",
                "curriculum vitae",
                "email",
                "phone",
                "mobile",
                "linkedin",
                "github",
                "@"
            ]
        ):

            continue

        words = line.split()

        if 2 <= len(words) <= 5:

            if all(
                any(char.isalpha() for char in word)
                for word in words
            ):

                return line

    return "Not detected"


# ============================================================
# EDUCATION EXTRACTION
# ============================================================

def extract_education(text):

    education_patterns = [

        r"\bB\.?\s*Tech\b",

        r"\bB\.?\s*E\b",

        r"\bBCA\b",

        r"\bM\.?\s*Tech\b",

        r"\bMCA\b",

        r"\bB\.?\s*Sc\b",

        r"\bM\.?\s*Sc\b",

        r"\bBachelor of Technology\b",

        r"\bBachelor of Engineering\b",

        r"\bComputer Science\b",

        r"\bInformation Technology\b"

    ]

    for pattern in education_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return match.group(0)

    return "Not detected"


# ============================================================
# GRADUATION YEAR EXTRACTION
# ============================================================

def extract_graduation_year(text):

    years = re.findall(
        r"\b20\d{2}\b",
        text
    )

    if not years:

        return "Not detected"

    # Remove duplicate years
    years = list(dict.fromkeys(years))

    # Usually the latest year is graduation year
    return years[-1]


# ============================================================
# SKILL DETECTION
# ============================================================

def detect_skills(text):

    text_lower = text.lower()

    detected_skills = set()


    skill_aliases = {

        "python": [
            "python"
        ],

        "sql": [
            "sql"
        ],

        "excel": [
            "excel",
            "microsoft excel"
        ],

        "power bi": [
            "power bi",
            "powerbi"
        ],

        "statistics": [
            "statistics",
            "statistical"
        ],

        "machine learning": [
            "machine learning",
            "machine-learning",
            "ml"
        ],

        "deep learning": [
            "deep learning",
            "deep-learning"
        ],

        "pandas": [
            "pandas"
        ],

        "numpy": [
            "numpy"
        ],

        "tensorflow": [
            "tensorflow"
        ],

        "scikit-learn": [
            "scikit-learn",
            "scikit learn",
            "sklearn"
        ],

        "java": [
            "java"
        ],

        "c": [
            "c programming",
            "c language"
        ],

        "c++": [
            "c++"
        ],

        "dsa": [
            "dsa",
            "data structures",
            "data structures and algorithms"
        ],

        "git": [
            "git"
        ],

        "github": [
            "github"
        ],

        "html": [
            "html",
            "html5"
        ],

        "css": [
            "css",
            "css3"
        ],

        "javascript": [
            "javascript",
            "java script",
            "js"
        ],

        "react": [
            "react",
            "reactjs",
            "react.js"
        ],

        "node.js": [
            "node.js",
            "nodejs",
            "node js"
        ],

        "django": [
            "django"
        ],

        "flask": [
            "flask"
        ],

        "spring boot": [
            "spring boot"
        ],

        "rest api": [
            "rest api",
            "restful api",
            "rest api development"
        ],

        "nlp": [
            "nlp",
            "natural language processing"
        ],

        "transformers": [
            "transformers",
            "transformer"
        ],

        "pytorch": [
            "pytorch"
        ],

        "etl": [
            "etl",
            "extract transform load"
        ],

        "pyspark": [
            "pyspark",
            "spark"
        ],

        "aws": [
            "aws",
            "amazon web services"
        ],

        "azure": [
            "azure",
            "microsoft azure"
        ],

        "linux": [
            "linux"
        ],

        "docker": [
            "docker"
        ],

        "kubernetes": [
            "kubernetes",
            "k8s"
        ],

        "jenkins": [
            "jenkins"
        ],

        "networking": [
            "networking",
            "computer networking"
        ],

        "cybersecurity": [
            "cybersecurity",
            "cyber security"
        ],

        "siem": [
            "siem"
        ],

        "mysql": [
            "mysql"
        ],

        "postgresql": [
            "postgresql",
            "postgres"
        ],

        "database management": [
            "database management",
            "database administration"
        ],

        "dax": [
            "dax"
        ],

        "data visualization": [
            "data visualization",
            "data visualisation"
        ],

        "selenium": [
            "selenium"
        ],

        "software testing": [
            "software testing",
            "software test",
            "software testing tools"
        ]

    }


    # --------------------------------------------------------
    # Search every skill
    # --------------------------------------------------------

    for skill, aliases in skill_aliases.items():

        for alias in aliases:

            pattern = (
                r"(?<!\w)"
                + re.escape(alias)
                + r"(?!\w)"
            )

            if re.search(
                pattern,
                text_lower
            ):

                detected_skills.add(
                    skill
                )

                break


    return detected_skills


# ============================================================
# JOB MATCH CALCULATION
# ============================================================

def calculate_job_match(
    student_skills,
    required_skills
):

    required = set(
        normalize_skill(skill)
        for skill in required_skills
    )

    matched = (
        student_skills
        .intersection(required)
    )

    missing = (
        required
        - student_skills
    )

    if required:

        percentage = (
            len(matched)
            / len(required)
        ) * 100

    else:

        percentage = 0


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

    st.session_state.student_name = "Not detected"


if "education" not in st.session_state:

    st.session_state.education = "Not detected"


if "graduation_year" not in st.session_state:

    st.session_state.graduation_year = "Not detected"


if "student_skills" not in st.session_state:

    st.session_state.student_skills = set()


# ============================================================
# RESUME UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "📄 Upload your Resume (PDF)",
    type=["pdf"]
)


if uploaded_file:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )


    if st.button(
        "🔍 Analyze Resume",
        type="primary"
    ):

        with st.spinner(
            "Analyzing your resume..."
        ):

            pdf_bytes = uploaded_file.read()

            resume_text = extract_resume_text(
                pdf_bytes
            )

            student_name = extract_name(
                resume_text
            )

            education = extract_education(
                resume_text
            )

            graduation_year = (
                extract_graduation_year(
                    resume_text
                )
            )

            student_skills = detect_skills(
                resume_text
            )


            # Save results
            st.session_state.resume_text = (
                resume_text
            )

            st.session_state.student_name = (
                student_name
            )

            st.session_state.education = (
                education
            )

            st.session_state.graduation_year = (
                graduation_year
            )

            st.session_state.student_skills = (
                student_skills
            )

            st.session_state.analysis_done = (
                True
            )


        st.success(
            "Resume analysis completed successfully! ✅"
        )
# ============================================================
# DISPLAY ANALYSIS RESULTS
# ============================================================

if st.session_state.analysis_done:

    student_skills = (
        st.session_state.student_skills
    )


    # ========================================================
    # STUDENT PROFILE
    # ========================================================

    st.header("👨‍🎓 Student Profile")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Name",
            st.session_state.student_name
        )

    with col2:

        st.metric(
            "Education",
            st.session_state.education
        )

    with col3:

        st.metric(
            "Graduation Year",
            st.session_state.graduation_year
        )


    # ========================================================
    # DETECTED SKILLS
    # ========================================================

    st.header("🧠 Detected Skills")

    if student_skills:

        sorted_skills = sorted(
            student_skills
        )

        # Display skills as separate badges
        skill_columns = st.columns(4)

        for index, skill in enumerate(
            sorted_skills
        ):

            with skill_columns[
                index % 4
            ]:

                st.success(
                    skill.title()
                )


        st.info(
            f"Total technical skills detected: "
            f"{len(student_skills)}"
        )

    else:

        st.warning(
            "No matching technical skills "
            "were detected from the resume."
        )


    # ========================================================
    # CAREER RECOMMENDATION ENGINE
    # ========================================================

    st.header("💼 Career Recommendations")

    recommendations = []


    for _, job in jobs.iterrows():

        required_skills = set(
            normalize_skill(skill)
            for skill in job[
                "required_skills"
            ].split(",")
        )


        matched_skills = (
            student_skills
            .intersection(required_skills)
        )


        if required_skills:

            match_percentage = (
                len(matched_skills)
                / len(required_skills)
            ) * 100

        else:

            match_percentage = 0


        recommendations.append({

            "Job Role":
                job["job_role"],

            "Match Percentage":
                match_percentage,

            "Matched Skills":
                len(matched_skills),

            "Required Skills":
                len(required_skills)

        })


    recommendations_df = pd.DataFrame(
        recommendations
    )


    recommendations_df = (
        recommendations_df
        .sort_values(
            by="Match Percentage",
            ascending=False
        )
        .reset_index(drop=True)
    )


    # ========================================================
    # TOP 5 CAREER ROLES
    # ========================================================

    st.subheader(
        "⭐ Top Career Matches"
    )


    top_5 = recommendations_df.head(5)


    for index, row in top_5.iterrows():

        percentage = row[
            "Match Percentage"
        ]

        role = row[
            "Job Role"
        ]


        st.write(
            f"### {index + 1}. {role}"
        )


        st.progress(
            int(percentage)
        )


        st.write(
            f"**Skill Match: "
            f"{percentage:.2f}%**"
        )


        st.caption(
            f"{int(row['Matched Skills'])} "
            f"of {int(row['Required Skills'])} "
            f"required skills matched."
        )


    # ========================================================
    # CAREER MATCH CHART
    # ========================================================

    st.subheader(
        "📊 Career Match Overview"
    )


    chart_df = top_5[
        [
            "Job Role",
            "Match Percentage"
        ]
    ].copy()


    chart_df = chart_df.set_index(
        "Job Role"
    )


    st.bar_chart(
        chart_df
    )


    # ========================================================
    # ALL CAREER ROLES
    # ========================================================

    with st.expander(
        "📋 View All Career Matches"
    ):

        display_df = recommendations_df.copy()

        display_df[
            "Match Percentage"
        ] = display_df[
            "Match Percentage"
        ].round(2)


        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


    # ========================================================
    # DETAILED SKILL GAP ANALYSIS
    # ========================================================

    st.header(
        "🔎 Detailed Skill Gap Analysis"
    )


    st.write(
        """
Choose any job role to see exactly which skills
you already have and which skills you need to learn.
"""
    )


    role_list = jobs[
        "job_role"
    ].tolist()


    selected_role = st.selectbox(
        "🎯 Choose a job role",
        role_list,
        key="selected_job_role"
    )


    # --------------------------------------------------------
    # Find selected job
    # --------------------------------------------------------

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
        .intersection(
            required_skills
        )
    )


    missing_skills = (
        required_skills
        - student_skills
    )


    if required_skills:

        match_percentage = (
            len(matched_skills)
            / len(required_skills)
        ) * 100

    else:

        match_percentage = 0


    # ========================================================
    # SELECTED ROLE SUMMARY
    # ========================================================

    st.subheader(
        f"🎯 {selected_role}"
    )


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


    # ========================================================
    # REQUIRED SKILLS
    # ========================================================

    st.write(
        "### 📋 Required Skills"
    )


    required_display = [
        skill.title()
        for skill in sorted(
            required_skills
        )
    ]


    st.write(
        " • ".join(required_display)
    )


    # ========================================================
    # MATCHED SKILLS
    # ========================================================

    st.write(
        "### ✅ Skills You Already Have"
    )


    if matched_skills:

        matched_columns = st.columns(4)


        for index, skill in enumerate(
            sorted(matched_skills)
        ):

            with matched_columns[
                index % 4
            ]:

                st.success(
                    f"✓ {skill.title()}"
                )

    else:

        st.info(
            "No required skills matched yet."
        )


    # ========================================================
    # MISSING SKILLS
    # ========================================================

    st.write(
        "### ❌ Skills You Need to Learn"
    )


    if missing_skills:

        missing_columns = st.columns(3)


        for index, skill in enumerate(
            sorted(missing_skills)
        ):

            with missing_columns[
                index % 3
            ]:

                st.warning(
                    f"📚 {skill.title()}"
                )

    else:

        st.success(
            "🎉 You already have all the "
            "required skills for this role!"
        )
# ============================================================
# PERSONALIZED LEARNING ROADMAP
# ============================================================

if st.session_state.analysis_done:

    st.header("🗺️ Personalized Learning Roadmap")

    st.write(
        f"""
Your learning roadmap is based on the skills required for
**{selected_role}** that are currently missing from your resume.
"""
    )

    if missing_skills:

        roadmap_rows = []

        for skill in sorted(missing_skills):

            roadmap_info = learning_roadmap.get(skill)

            if roadmap_info:

                roadmap_rows.append({
                    "Skill": skill.title(),
                    "Phase": roadmap_info["phase"],
                    "Duration": roadmap_info["duration"],
                    "Project": roadmap_info["project"]
                })

            else:

                roadmap_rows.append({
                    "Skill": skill.title(),
                    "Phase": "Learning",
                    "Duration": "Self-paced",
                    "Project": "Build a practical project"
                })

        roadmap_df = pd.DataFrame(roadmap_rows)

        st.subheader("📅 Roadmap Overview")

        st.dataframe(
            roadmap_df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("📖 Step-by-Step Learning Plan")

        step_number = 1

        for skill in sorted(missing_skills):

            roadmap_info = learning_roadmap.get(skill)

            with st.expander(
                f"🚀 Step {step_number}: Learn {skill.title()}"
            ):

                if roadmap_info:

                    st.markdown(
                        f"**🎯 Learning Phase:** "
                        f"{roadmap_info['phase']}"
                    )

                    st.markdown(
                        f"**⏱️ Estimated Duration:** "
                        f"{roadmap_info['duration']}"
                    )

                    st.markdown(
                        "### 📚 Topics to Learn"
                    )

                    topics = roadmap_info.get(
                        "topics",
                        []
                    )

                    # FIX: Always treat topics as a list
                    if isinstance(topics, str):

                        topics = [
                            topic.strip()
                            for topic in topics.split(",")
                            if topic.strip()
                        ]

                    for topic in topics:

                        st.markdown(
                            f"• {topic}"
                        )

                    st.markdown(
                        "### 🛠️ Recommended Project"
                    )

                    st.info(
                        roadmap_info["project"]
                    )

                else:

                    st.markdown(
                        "### 📚 Topics to Learn"
                    )

                    st.write(
                        "• Learn the fundamentals"
                    )

                    st.write(
                        "• Practice important concepts"
                    )

                    st.write(
                        "• Solve practical problems"
                    )

                    st.write(
                        "• Build a small project"
                    )

                    st.markdown(
                        "### 🛠️ Recommended Project"
                    )

                    st.info(
                        f"Build a practical project "
                        f"using {skill.title()}."
                    )

            step_number += 1
# ====================================================
        # FINAL CAREER PROJECT
        # ====================================================

        st.subheader("🚀 Final Career Project")

        st.write(
            f"""
After completing the missing skills for
**{selected_role}**, combine multiple skills into
one practical project.
"""
        )

        st.success(
            f"""
💡 **Suggested Project Strategy**

Build a project related to **{selected_role}**
that demonstrates multiple required skills.

Your project should include:

• Practical problem solving
• Real-world dataset or application
• Multiple technical skills
• User-friendly interface
• GitHub documentation
• Project screenshots
• Clear project explanation
"""
        )

        # ====================================================
        # CAREER DEVELOPMENT
        # ====================================================

        st.header("🚀 Career Development Suggestion")

        missing_display = ", ".join(
            skill.title()
            for skill in sorted(missing_skills)
        )

        st.info(
            f"""
### 🎯 Your Focus Area

For **{selected_role}**, focus on learning:

**{missing_display}**

### 📌 Recommended Strategy

1. Learn the fundamentals.
2. Practice each skill.
3. Complete the recommended projects.
4. Build one combined real-world project.
5. Upload the project to GitHub.
6. Add the project to your resume.
7. Practice technical interviews.
8. Prepare for aptitude and assessment rounds.
"""
        )

    else:

        # ====================================================
        # NO SKILL GAP
        # ====================================================

        st.success(
            f"""
🎉 Your current resume contains all the listed
skills required for **{selected_role}**.
"""
        )

        st.info(
            """
### 📌 Recommended Next Steps

• Learn advanced concepts
• Build real-world projects
• Practice DSA
• Improve your GitHub portfolio
• Prepare technical interviews
• Practice aptitude assessments
• Apply for internships and jobs
"""
        )

    # ========================================================
    # ANALYSIS SUMMARY
    # ========================================================

    st.header("📊 Analysis Summary")

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:

        st.metric(
            "Skills Detected",
            len(student_skills)
        )

    with summary_col2:

        st.metric(
            "Selected Role Match",
            f"{match_percentage:.1f}%"
        )

    with summary_col3:

        st.metric(
            "Skills to Learn",
            len(missing_skills)
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
### 🎯 AI-Powered Skill Gap Analyzer

**Technologies:**  
Python • NLP • Machine Learning • Pandas • PyMuPDF • RapidOCR • Streamlit

**Project Purpose:**  
Analyze resumes, identify technical skills, recommend career
roles, identify skill gaps, and generate personalized
learning roadmaps.
"""
)

st.caption(
    "Final Year B.Tech CSE Project | "
    "AI-Powered Career Recommendation System"
)            