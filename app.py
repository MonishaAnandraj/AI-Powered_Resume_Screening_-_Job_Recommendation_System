import streamlit as st
import PyPDF2
import docx2txt
import nltk
import tempfile
import pandas as pd
import matplotlib.pyplot as plt

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from wordcloud import WordCloud

# ----------------------------
# NLTK Downloads
# ----------------------------

nltk.download('stopwords')
nltk.download('punkt')

# ----------------------------
# Skills Database
# ----------------------------

SKILLS_DB = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "tensorflow",
    "keras",
    "pandas",
    "numpy",
    "power bi",
    "tableau",
    "excel",
    "aws",
    "azure",
    "docker",
    "git",
    "github",
    "flask",
    "streamlit",
    "react",
    "nodejs",
    "mysql",
    "statistics",
    "data analysis",
    "data science",
    "nlp",
    "scikit learn",
    "matplotlib",
    "seaborn"
]

# ----------------------------
# Job Database
# ----------------------------

JOBS = {
    "Data Analyst":
        ["python", "sql", "excel", "power bi"],

    "Data Scientist":
        ["python", "machine learning",
         "pandas", "numpy"],

    "Machine Learning Engineer":
        ["python", "tensorflow",
         "keras", "aws"],

    "Business Analyst":
        ["sql", "excel",
         "power bi"],

    "AI Engineer":
        ["python", "nlp",
         "machine learning",
         "deep learning"],

    "Full Stack Developer":
        ["react", "nodejs",
         "mysql", "git"]
}

# ----------------------------
# PDF Reader
# ----------------------------

def extract_text_from_pdf(uploaded_file):

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    text = ""

    for page in pdf_reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text

# ----------------------------
# DOCX Reader
# ----------------------------

def extract_text_from_docx(uploaded_file):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".docx"
    ) as tmp:

        tmp.write(uploaded_file.read())

        tmp_path = tmp.name

    text = docx2txt.process(tmp_path)

    return text

# ----------------------------
# Preprocessing
# ----------------------------

def preprocess_text(text):

    stop_words = set(
        stopwords.words('english')
    )

    word_tokens = word_tokenize(
        text.lower()
    )

    filtered_tokens = [

        word

        for word in word_tokens

        if word.isalpha()

        and word not in stop_words
    ]

    return filtered_tokens

# ----------------------------
# Similarity Score
# ----------------------------

def calculate_similarity(
        resume_text,
        jd_text
):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        [resume_text, jd_text]
    )

    similarity_score = cosine_similarity(
        vectors
    )[0][1]

    return similarity_score

# ----------------------------
# Skill Extraction
# ----------------------------

def extract_skills(text):

    text = text.lower()

    skills_found = []

    for skill in SKILLS_DB:

        if skill in text:

            skills_found.append(skill)

    return list(set(skills_found))

# ----------------------------
# Job Recommendation
# ----------------------------

def recommend_jobs(user_skills):

    recommendations = []

    for job, skills in JOBS.items():

        overlap = len(
            set(user_skills)
            &
            set(skills)
        )

        recommendations.append(
            (job, overlap)
        )

    recommendations.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return recommendations

# ----------------------------
# Resume Analysis
# ----------------------------

def analyze_resume(score):

    if score >= 80:
        return "Excellent Match"

    elif score >= 60:
        return "Good Match"

    elif score >= 40:
        return "Average Match"

    else:
        return "Needs Improvement"

# ----------------------------
# Word Cloud
# ----------------------------

def generate_wordcloud(text):

    wc = WordCloud(
        width=800,
        height=400,
        background_color="white"
    ).generate(text)

    fig, ax = plt.subplots()

    ax.imshow(wc)

    ax.axis("off")

    return fig

# ----------------------------
# Streamlit UI
# ----------------------------

st.set_page_config(
    page_title="AI Resume Screening System",
    layout="wide"
)

st.markdown("""
<style>

/* Main App */
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b
    );
    color: white;
}

/* Headers */
h1 {
    color: #38bdf8 !important;
    text-align: center;
    font-weight: 700;
}

h2, h3 {
    color: #f8fafc !important;
}

/* Upload Boxes */
[data-testid="stFileUploader"] {
    background-color: #1e293b;
    border-radius: 15px;
    padding: 15px;
    border: 2px solid #38bdf8;
}

/* Metric Cards */
.metric-card {
    background: #1e293b;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 0px 10px rgba(56,189,248,0.3);
}

/* Skill Badges */
.skill-badge {
    background: #10b981;
    color: white;
    padding: 8px 15px;
    border-radius: 20px;
    margin: 5px;
    display: inline-block;
    font-weight: bold;
}

/* Missing Skills */
.missing-badge {
    background: #ef4444;
    color: white;
    padding: 8px 15px;
    border-radius: 20px;
    margin: 5px;
    display: inline-block;
    font-weight: bold;
}

/* Job Cards */
.job-card {
    background: #1e293b;
    padding: 10px;
    border-radius: 15px;
    margin-bottom: 10px;
    border-left: 5px solid #38bdf8;
    box-shadow: 0px 0px 10px rgba(56,189,248,0.3);
}

/* Tabs */
button[data-baseweb="tab"] {
    font-size: 16px;
    font-weight: bold;
}

/* Buttons */
.stButton > button {
    width: 100%;
    background: linear-gradient(
        90deg,
        #06b6d4,
        #3b82f6
    );
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px;
    font-size: 18px;
    font-weight: bold;
}

.stButton > button:hover {
    background: linear-gradient(
        90deg,
        #3b82f6,
        #06b6d4
    );
    transform: scale(1.02);
}

/* Text Areas */
textarea {
    border-radius: 10px !important;
}

/* Hide Streamlit Menu */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

st.title(
    "📄 AI Resume Screening & Job Recommendation System"
)

st.markdown(
    "Upload Resume and Job Description"
)

resume_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

jd_file = st.file_uploader(
    "Upload Job Description",
    type=["pdf", "docx"]
)

if st.button("Analyze Resume"):

    if resume_file is None or jd_file is None:

        st.error(
            "Please upload both files."
        )

    else:

        # Resume

        if resume_file.name.endswith(
                ".pdf"):

            resume_text = \
                extract_text_from_pdf(
                    resume_file
                )

        else:

            resume_text = \
                extract_text_from_docx(
                    resume_file
                )

        # JD

        if jd_file.name.endswith(
                ".pdf"):

            jd_text = \
                extract_text_from_pdf(
                    jd_file
                )

        else:

            jd_text = \
                extract_text_from_docx(
                    jd_file
                )

        # NLP

        pre_resume = preprocess_text(
            resume_text
        )

        pre_jd = preprocess_text(
            jd_text
        )

        similarity_score = \
            calculate_similarity(
                " ".join(pre_resume),
                " ".join(pre_jd)
            )

        percentage = round(
            similarity_score * 100,
            2
        )

        # Score

        st.subheader(
            "Resume Match Score"
        )

        st.progress(
            min(int(percentage), 100)
        )

        st.success(
            f"{percentage}% Match"
        )

        # Resume Analysis

        st.subheader(
            "Resume Analysis"
        )

        st.info(
            analyze_resume(
                percentage
            )
        )

        # Skills

        resume_skills = \
            extract_skills(
                resume_text
            )

        jd_skills = \
            extract_skills(
                jd_text
            )

        missing_skills = list(
            set(jd_skills)
            -
            set(resume_skills)
        )

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "Resume Skills"
            )

            skills_html = ""

            for skill in resume_skills:
                skills_html += f"""
                <span class="skill-badge">
                    {skill}
                </span>
                """

            st.markdown(
                skills_html,
                unsafe_allow_html=True
            )

        with col2:

            st.subheader(
                "Missing Skills"
            )

            if missing_skills:

                missing_html = ""

                for skill in missing_skills:
                    missing_html += f"""
                    <span class="missing-badge">
                        {skill}
                    </span>
                    """

                st.markdown(
                    missing_html,
                    unsafe_allow_html=True
                )

            else:

                st.success(
                    "No Missing Skills"
                )

        # Job Recommendation

        st.subheader(
            "Recommended Jobs"
        )

        recommendations = \
            recommend_jobs(
                resume_skills
            )

        for job, score in recommendations[:5]:

            st.markdown(f"""
              <div class="job-card">

                ### 💼 {job}

                Matching Skills: {score}

                </div>
            """, unsafe_allow_html=True)

        # Charts

        if len(jd_skills) > 0:

            skill_match = round(
                (
                    len(
                        set(resume_skills)
                        &
                        set(jd_skills)
                    )
                    /
                    len(jd_skills)
                ) * 100,
                2
            )

        else:

            skill_match = 0

        chart_data = pd.DataFrame({

            "Category": [
                "Similarity",
                "Skill Match"
            ],

            "Score": [
                percentage,
                skill_match
            ]
        })

        st.subheader(
            "Performance Metrics"
        )

        st.bar_chart(
            chart_data.set_index(
                "Category"
            )
        )

        # Word Clouds

        st.subheader(
            "Word Clouds"
        )

        c1, c2 = st.columns(2)

        with c1:

            st.write(
                "Resume Word Cloud"
            )

            st.pyplot(
                generate_wordcloud(
                    resume_text
                )
            )

        with c2:

            st.write(
                "JD Word Cloud"
            )

            st.pyplot(
                generate_wordcloud(
                    jd_text
                )
            )