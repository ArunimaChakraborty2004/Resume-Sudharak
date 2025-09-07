from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib import colors
import tempfile
import textwrap
import logging

logger = logging.getLogger(__name__)

def export_feedback_as_pdf(feedback_text: str) -> str:
    """
    Export feedback text to a well-formatted PDF.
    """
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_path = temp_file.name
        temp_file.close()
        
        doc = SimpleDocTemplate(temp_path, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=72)
        
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = styles['Title']
        title = Paragraph("Resume Feedback Report", title_style)
        story.append(title)
        story.append(Spacer(1, 0.3 * inch))
        
        # Process feedback text
        lines = feedback_text.split('\n')
        current_section = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect headers
            if (line.startswith('##') or 
                (len(line) < 50 and (line.isupper() or line.endswith(':')) and not line.startswith('-'))):
                # Add previous section
                if current_section:
                    story.append(Paragraph('<br/>'.join(current_section), styles['BodyText']))
                    story.append(Spacer(1, 0.1 * inch))
                    current_section = []
                
                # Add header
                header_text = line.replace('##', '').strip()
                header = Paragraph(f"<b>{header_text}</b>", styles['Heading2'])
                story.append(header)
                story.append(Spacer(1, 0.1 * inch))
            else:
                # Regular content
                if line.startswith('- '):
                    line = f"• {line[2:]}"
                current_section.append(line)
        
        # Add final section
        if current_section:
            story.append(Paragraph('<br/>'.join(current_section), styles['BodyText']))
        
        doc.build(story)
        return temp_path
        
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        return export_feedback_simple(feedback_text)

def export_feedback_simple(feedback_text: str) -> str:
    """
    Simple fallback PDF export method.
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp_file.name, pagesize=letter)
    
    y_position = 750
    line_height = 14
    margin = 40
    width = letter[0] - 2 * margin
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y_position, "Resume Feedback Report")
    y_position -= 2 * line_height
    
    # Content
    c.setFont("Helvetica", 10)
    lines = feedback_text.split('\n')
    
    for line in lines:
        if y_position < margin + line_height:
            c.showPage()
            c.setFont("Helvetica", 10)
            y_position = 750
        
        wrapped_lines = textwrap.wrap(line, width=100)
        for wrapped_line in wrapped_lines:
            c.drawString(margin, y_position, wrapped_line)
            y_position -= line_height
        
        y_position -= 2  # Small space between lines
    
    c.save()
    return temp_file.name