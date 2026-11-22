
import fitz
from docx import Document
import io


def extract_text_from_pdf(file):
    """Extract text from PDF resume."""
    try:
        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
        text = ""

        for page in pdf_document:
            text += page.get_text()

        pdf_document.close()
        return text

    except Exception as e:
        raise ValueError(f"Error reading PDF: {e}")


def extract_text_from_docx(file):
    """Extract text from DOCX resume."""
    try:
        document = Document(io.BytesIO(file.read()))
        text = "\n".join(
            paragraph.text for paragraph in document.paragraphs
        )
        return text

    except Exception as e:
        raise ValueError(f"Error reading DOCX: {e}")


def extract_resume_text(file):
    """Extract text based on uploaded file type."""
    filename = file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)

    elif filename.endswith(".docx"):
        return extract_text_from_docx(file)

    else:
        raise ValueError("Please upload a PDF or DOCX resume.")
