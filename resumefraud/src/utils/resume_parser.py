import PyPDF2
import docx
import io

async def parse_resume(content: bytes, filename: str) -> str:
    if filename.endswith('.pdf'):
        return parse_pdf(content)
    elif filename.endswith('.docx'):
        return parse_docx(content)
    else:
        raise ValueError("Unsupported file format")

def parse_pdf(content):
    pdf_file = io.BytesIO(content)
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def parse_docx(content):
    doc = docx.Document(io.BytesIO(content))
    return " ".join([paragraph.text for paragraph in doc.paragraphs])
