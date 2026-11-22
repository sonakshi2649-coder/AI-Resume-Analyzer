
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Skills database
SKILLS = [
    "python", "java", "javascript", "c++", "c",
    "html", "css", "react", "angular", "node.js",
    "sql", "mysql", "mongodb", "postgresql",
    "machine learning", "deep learning", "artificial intelligence",
    "data analysis", "data science", "nlp",
    "pandas", "numpy", "scikit-learn", "tensorflow",
    "pytorch", "power bi", "tableau", "excel",
    "git", "github", "docker", "aws", "azure",
    "spring boot", "django", "flask", "fastapi",
    "rest api", "api", "oop", "data structures",
    "algorithms", "communication", "teamwork",
    "problem solving", "leadership"
]


def extract_skills(text):
    """Find skills mentioned in the given text."""

    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


def calculate_similarity(resume_text, job_description):
    """Calculate text similarity using TF-IDF."""

    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        vectors[0:1], vectors[1:2]
    )[0][0]

    return round(float(similarity) * 100, 2)


def analyze_resume(resume_text, job_description):
    """Analyze resume against job description."""

    if not resume_text.strip():
        raise ValueError("Resume text is empty.")

    if not job_description.strip():
        raise ValueError("Job description is empty.")

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched_skills = [
        skill for skill in job_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill for skill in job_skills
        if skill not in resume_skills
    ]

    if job_skills:
        skill_score = (
            len(matched_skills) / len(job_skills)
        ) * 100
    else:
        skill_score = 0

    text_score = calculate_similarity(
        resume_text, job_description
    )

    # Combined matching score
    match_score = (
        0.6 * skill_score + 0.4 * text_score
    )

    suggestions = []

    if missing_skills:
        suggestions.append(
            "Consider learning or demonstrating these skills: "
            + ", ".join(missing_skills)
        )

    if len(resume_skills) < 5:
        suggestions.append(
            "Add more relevant technical skills to your resume."
        )

    if not suggestions:
        suggestions.append(
            "Your resume covers the identified job skills well. "
            "Keep improving your project descriptions."
        )

    return {
        "match_score": round(match_score, 2),
        "skill_score": round(skill_score, 2),
        "text_score": round(text_score, 2),
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions
    }
