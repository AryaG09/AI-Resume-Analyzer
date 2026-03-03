import streamlit as st
import pdfplumber

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title(" AI Resume Analyzer & Career Guide")

st.markdown("""
Smart AI-powered tool to analyze resumes, match job roles, and identify skill gaps.
""")

st.markdown("---")

# ---------------- SKILL DATABASE ----------------
skills_db = [
    "python","java","c++","machine learning","deep learning",
    "data analysis","sql","excel","html","css","javascript",
    "react","node","communication","teamwork","leadership",
    "tensorflow","pandas","numpy","scikit-learn",
    "data structures","algorithms"
]

job_roles = {
    "data scientist": ["python","machine learning","sql","pandas","numpy"],
    "web developer": ["html","css","javascript","react"],
    "software engineer": ["python","java","c++","data structures","algorithms"],
    "data analyst": ["excel","sql","python","data analysis"]
}

# ---------------- FUNCTIONS ----------------
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()
    return text

def detect_skills(text):
    text = text.lower()
    found = []
    for skill in skills_db:
        if skill in text:
            found.append(skill)
    return found

def match_skills(user_skills, role):
    role = role.lower()
    if role in job_roles:
        required = job_roles[role]
        matched = [s for s in user_skills if s in required]
        score = int((len(matched)/len(required))*100)
        return matched, required, score
    return [], [], 0

# ---------------- UI INPUT ----------------
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_role = st.text_input("Enter target job role (e.g., software engineer)")

# ---------------- PROCESSING ----------------
if uploaded_file:
    st.success("Resume uploaded successfully!")

    resume_text = extract_text_from_pdf(uploaded_file)
    skills_found = detect_skills(resume_text)

    st.markdown("##  Detected Skills")

    cols = st.columns(4)
    for i, skill in enumerate(skills_found):
        cols[i % 4].markdown(
            f"<div style='background-color:#1f2937;padding:10px;border-radius:8px;text-align:center;color:white'>{skill}</div>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    if job_role:
        matched, required, score = match_skills(skills_found, job_role)

        st.markdown("##  Job Match Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ✅ Matched Skills")
            for skill in matched:
                st.markdown(f"- {skill}")

        with col2:
            st.markdown("### 📌 Required Skills")
            for skill in required:
                st.markdown(f"- {skill}")

        st.markdown("---")

        st.markdown("##  Resume Strength")

        if score >= 75:
            st.success(f"Strong Profile — {score}% Match ✅")
        elif score >= 50:
            st.warning(f"Moderate Profile — {score}% Match ⚠")
        else:
            st.error(f"Needs Improvement — {score}% Match ❌")

        st.progress(score)

        missing = [s for s in required if s not in skills_found]

        missing = [s for s in required if s not in skills_found]

    if missing:
     st.markdown("## Skills to Improve")

    cols = st.columns(min(3, len(missing)))

    for i, m in enumerate(missing):
        cols[i % len(cols)].markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #6D28D9, #4C1D95);
                padding: 15px;
                border-radius: 12px;
                text-align: center;
                color: white;
                font-weight: 500;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            ">
                {m}
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")
st.caption("Built by Arya Gawas | AI Resume Analyzer Project")