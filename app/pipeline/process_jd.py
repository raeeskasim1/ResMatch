from app.preprocessing.clean_text import clean_text
from app.extraction.skill_extractor import extract_skills
from app.extraction.education_extractor import extract_education
from app.extraction.experience_extractor import extract_jd_experience


def process_jd(jd_text: str, skills_list: list) -> dict:
    cleaned = clean_text(jd_text)

    return {
        "cleaned_text": cleaned,
        "skills": extract_skills(cleaned, skills_list),
        "education": extract_education(cleaned),
        "experience": extract_jd_experience(cleaned)
    }