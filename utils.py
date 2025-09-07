

import pdfplumber
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import streamlit as st

def extract_text_from_pdf(pdf_file):
    try:
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        st.error(f"❌ PDF extraction failed: {e}")
        return ""

def extract_text_from_docx(docx_file):
    try:
        doc = Document(docx_file)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    except Exception as e:
        st.error(f"❌ DOCX extraction failed: {e}")
        return ""

def export_feedback_as_pdf(feedback_text):
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        c = canvas.Canvas(temp_file.name, pagesize=letter)
        text_object = c.beginText(40, 750)
        text_object.setFont("Helvetica", 12)

        for line in feedback_text.split('\n'):
            text_object.textLine(line)

        c.drawText(text_object)
        c.save()
        return temp_file.name
    except Exception as e:
        st.error(f"❌ PDF export failed: {e}")
        return None
