import os
from app.ingestion.pdf_parser import extract_text_from_pdf
from app.ingestion.docx_parser import extract_text_from_docx
from app.ingestion.txt_parser import extract_text_from_txt


def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")