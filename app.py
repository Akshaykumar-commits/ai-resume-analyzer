import streamlit as st
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and paste the job description")

# ---------------- FUNCTIONS ----------------
def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
        return text.lower()
    except PdfReadError:
        return None
    except Exception:
        return None


def analyze_resume(resume_text, job_description):
    job_description = job_description.lower()

    skills = [
        "python", "java", "c",
        "data", "data structures",
        "ai", "machine learning",
        "problem solving",
        "project", "web"
    ]

    matched = []
    missing = []

    for skill in skills:
        if skill in resume_text:
            matched.append(skill)
        else:
            missing.append(skill)

    match_percentage = int((len(matched) / len(skills)) * 100)

    result = f"""
📊 *Match Percentage:* {match_percentage}%

✅ *Matched Skills:*
{', '.join(matched) if matched else 'None'}

❌ *Missing Skills:*
{', '.join(missing) if missing else 'None'}

💡 *Suggestions:*
Add the missing skills and small related projects to improve your resume.
"""

    return result


# ---------------- UI ----------------
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_desc = st.text_area("Paste Job Description", height=180)

if st.button("🔍 Analyze Resume"):
    if resume_file and job_desc.strip():
        with st.spinner("Analyzing your resume..."):
            resume_text = extract_text_from_pdf(resume_file)

        if resume_text is None or resume_text.strip() == "":
            st.error(
                "❌ Unable to read this PDF.\n\n"
                "Please upload a *text-based PDF* (not scanned or image-only).\n"
                "Tip: Export your resume from Word / Google Docs as PDF."
            )
        else:
            analysis_result = analyze_resume(resume_text, job_desc)
            st.success("Analysis Complete ✅")
            st.markdown(analysis_result)
    else:
        st.warning("Please upload a resume and paste the job description")