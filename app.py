
import streamlit as st
from resume_parser import extract_resume_text
from analyzer import analyze_resume


from io import BytesIO
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf_report(results):
    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    content = []

    content.append(
        Paragraph("AI Resume Analyzer Report", styles["Title"])
    )
    content.append(Spacer(1, 20))

    content.append(Paragraph(
        f"Overall Match Score: {escape(str(results['match_score']))}%",
        styles["Heading2"]
    ))

    content.append(Paragraph(
        f"Skill Match: {escape(str(results['skill_score']))}%",
        styles["Normal"]
    ))

    content.append(Paragraph(
        f"Text Similarity: {escape(str(results['text_score']))}%",
        styles["Normal"]
    ))

    content.append(Spacer(1, 20))

    content.append(
        Paragraph("Matched Skills", styles["Heading2"])
    )

    for skill in results["matched_skills"]:
        content.append(
            Paragraph("- " + escape(str(skill).title()), styles["Normal"])
        )

    content.append(Spacer(1, 15))

    content.append(
        Paragraph("Missing Skills", styles["Heading2"])
    )

    for skill in results["missing_skills"]:
        content.append(
            Paragraph("- " + escape(str(skill).title()), styles["Normal"])
        )

    content.append(Spacer(1, 15))

    content.append(
        Paragraph("Improvement Suggestions", styles["Heading2"])
    )

    for suggestion in results["suggestions"]:
        content.append(
            Paragraph("- " + escape(str(suggestion)), styles["Normal"])
        )

    pdf.build(content)

    return buffer.getvalue()


# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #f8f9fc;
}
.title {
    font-size: 42px;
    font-weight: 800;
    color: #243b64;
    text-align: center;
}
.subtitle {
    text-align: center;
    color: #64748b;
    font-size: 18px;
}
.result-card {
    background-color: #ffffff;
    padding: 22px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
}
</style>
""", unsafe_allow_html=True)


# Header
st.markdown(
    '<div class="title">📄 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze your resume against a job description '
    'and discover opportunities to improve.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# Sidebar
with st.sidebar:
    st.title("About")
    st.write(
        "AI Resume Analyzer helps candidates understand "
        "how well their resume matches a job description."
    )

    st.info(
        "Upload your PDF or DOCX resume and paste "
        "the job description to get started."
    )

    st.caption("Built with Python and Streamlit")


# Main input section
st.subheader("1. Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf", "docx"],
    help="Supported formats: PDF and DOCX"
)

st.subheader("2. Enter Job Description")

job_description = st.text_area(
    "Paste the job description here",
    height=220,
    placeholder=(
        "Example: We are looking for a Python Developer "
        "with knowledge of Python, SQL, Django, Git..."
    )
)

# Analyze button
if st.button("🔍 Analyze Resume", type="primary",
             use_container_width=True):

    if uploaded_file is None:
        st.error("Please upload your resume first.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:
        try:
            with st.spinner("Analyzing your resume..."):

                resume_text = extract_resume_text(uploaded_file)

                if not resume_text.strip():
                    st.error(
                        "No readable text found. "
                        "Please upload a text-based PDF or DOCX."
                    )
                else:
                    results = analyze_resume(
                        resume_text,
                        job_description
                    )

                    st.success("Resume analysis completed!")

                    st.divider()
                    st.header("📊 Analysis Results")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Overall Match Score",
                            f"{results['match_score']}%"
                        )

                    with col2:
                        st.metric(
                            "Skill Match",
                            f"{results['skill_score']}%"
                        )

                    with col3:
                        st.metric(
                            "Text Similarity",
                            f"{results['text_score']}%"
                        )

                    st.progress(
                        min(results["match_score"] / 100, 1.0)
                    )

                    st.divider()

                    left, right = st.columns(2)

                    with left:
                        st.subheader("✅ Matched Skills")

                        if results["matched_skills"]:
                            for skill in results["matched_skills"]:
                                st.write(f"🟢 {skill.title()}")
                        else:
                            st.info("No matching skills found.")

                    with right:
                        st.subheader("❌ Missing Skills")

                        if results["missing_skills"]:
                            for skill in results["missing_skills"]:
                                st.write(f"🔴 {skill.title()}")
                        else:
                            st.success("No missing skills detected!")

                    st.divider()

                    st.subheader("💡 Improvement Suggestions")

                    for suggestion in results["suggestions"]:
                        st.write(f"• {suggestion}")

                    with st.expander("View All Extracted Resume Skills"):
                        st.write(results["resume_skills"])

                    with st.expander("View Job Description Skills"):
                        st.write(results["job_skills"])

                    st.divider()

                    st.subheader("📥 Download Your Report")

                    pdf_file = create_pdf_report(results)

                    st.download_button(
                        label="Download Analysis Report (PDF)",
                        data=pdf_file,
                        file_name="AI_Resume_Analysis_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )


        except Exception as error:
            st.error(f"Something went wrong: {error}")


st.divider()

st.caption(
    "AI Resume Analyzer | Built using Python, "
    "Scikit-learn and Streamlit"
)
