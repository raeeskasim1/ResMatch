import os
from app.ingestion.file_loader import extract_text
from app.preprocessing.clean_text import clean_text, clean_summary_text
from app.preprocessing.section_splitter import split_sections
from app.extraction.skill_extractor import load_skills, extract_skills
from app.extraction.education_extractor import extract_education
from app.extraction.experience_extractor import extract_resume_experience
from app.extraction.name_extractor import extract_name
from app.embeddings.embedder import TextEmbedder
from app.vectordb.resume_store import add_resume

SKILL_FILE = "data/skills_master.txt"
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def process_resume_text(text: str, skills_list: list) -> dict:
    """
    Process raw resume text and extract structured candidate information.

    Args:
        text (str): Raw text extracted from a resume file.
        skills_list (list): Master list of skills used for skill extraction.

    Returns:
        dict: Processed resume data including candidate name, cleaned text,
        split sections, extracted skills, education, and experience.
    """
    cleaned = clean_text(text)
    sections = split_sections(text)

    return {
        "name": extract_name(text),
        "cleaned_text": cleaned,
        "sections": sections,
        "skills": extract_skills(cleaned, skills_list),
        "education": extract_education(cleaned),
        "experience": extract_resume_experience(sections.get("experience", ""))
    }


def index_resumes(file_paths: list):
    """
    Parse, preprocess, embed, and store multiple resumes in the vector database.

    This function validates supported files, extracts resume text, generates
    embeddings, prepares metadata, and stores each processed resume in the
    vector database.

    Args:
        file_paths (list): List of resume file paths to index.

    Returns:
        None
    """
    skills_list = load_skills(SKILL_FILE)
    embedder = TextEmbedder()

    processed_resumes = []
    resume_texts = []

    for file_path in file_paths:
        file_name = os.path.basename(file_path)

        if not os.path.isfile(file_path):
            continue

        ext = os.path.splitext(file_name)[1].lower()

        if file_name.startswith("~$"):
            print(f"Skipped temp file: {file_name}")
            continue

        if ext not in ALLOWED_EXTENSIONS:
            print(f"Skipped unsupported file: {file_name}")
            continue

        try:
            raw_text = extract_text(file_path)
            data = process_resume_text(raw_text, skills_list)

            processed_resumes.append({
                "file_name": file_name,
                "data": data
            })
            resume_texts.append(data["cleaned_text"])

        except Exception as e:
            print(f"Failed for {file_name}: {e}")

    if not resume_texts:
        return

    embeddings = embedder.encode_many(resume_texts, batch_size=32)

    for item, embedding in zip(processed_resumes, embeddings):
        file_name = item["file_name"]
        data = item["data"]

        resume_id = data["name"]
        raw_summary = data["sections"].get("summary", "").strip()
        clean_summary = clean_summary_text(raw_summary)

        metadata = {
            "file_name": file_name,
            "candidate_name": data["name"],
            "summary": clean_summary,
            "skills": ",".join(data["skills"]),
            "education": ",".join(data["education"]),
            "experience_years": data["experience"]
        }

        add_resume(
            resume_id=resume_id,
            document=data["cleaned_text"],
            embedding=embedding,
            metadata=metadata
        )

        print(f"Indexed: {file_name} | Name: {data['name']}")