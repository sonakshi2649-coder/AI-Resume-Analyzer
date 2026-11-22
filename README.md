# AI Resume Analyzer 📄

An NLP-based Resume Analyzer built using Python and Streamlit. It analyzes resumes against job descriptions and provides match scores, skill comparisons, and improvement suggestions.

## 🚀 Features

- Upload resumes in PDF and DOCX formats.
- Extract text from uploaded resumes.
- Analyze resumes against job descriptions.
- Calculate Overall Match Score.
- Calculate Skill Match and Text Similarity.
- Identify Matched Skills and Missing Skills.
- Provide Resume Improvement Suggestions.
- Download the analysis report as a PDF.

## 🛠️ Technologies Used

- Python
- Streamlit
- PyMuPDF
- python-docx
- Scikit-learn
- Pandas
- NumPy
- ReportLab

## ⚙️ Installation and Setup

1. Clone the repository:

   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   ```

2. Navigate to the project folder:

   ```bash
   cd AI-Resume-Analyzer
   ```

3. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Run the application:

   ```bash
   python -m streamlit run app.py
   ```

## 📊 How It Works

1. Upload your resume.
2. Paste the job description.
3. Click Analyze Resume.
4. View your match score and skill analysis.
5. Download your PDF analysis report.

## 🧠 Analysis Method

The project uses keyword-based skill extraction and TF-IDF with cosine similarity to compare resume content with job descriptions.

## ⚠️ Limitations

- Scanned image-only PDFs may not be readable.
- Skill matching depends on the project's predefined skill list.
- Match scores are indicative and do not guarantee job selection.

## 👩‍💻 Author

Developed as a Python-based resume analysis project.