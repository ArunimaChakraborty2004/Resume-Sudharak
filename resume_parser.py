import pdfplumber
import docx
import io
import logging
import fitz

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text from PDF file.
    """
    try:
        text = ""
        with pdfplumber.open(io.BytesIO(pdf_file.read())) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise Exception(f"Failed to extract text from PDF: {str(e)}")

def extract_text_from_docx(docx_file) -> str:
    """
    Extract text from DOCX file.
    """
    try:
        doc = docx.Document(io.BytesIO(docx_file.read()))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {e}")
        raise Exception(f"Failed to extract text from DOCX: {str(e)}")



def highlight_resume_sections(pdf_file, keywords):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page in doc:
        for kw in keywords:
            areas = page.search_for(kw)
            for area in areas:
                page.draw_rect(area, color=(1, 0, 0), fill=(1, 0.8, 0.8))  # red highlight
    doc.save("highlighted_resume.pdf")
