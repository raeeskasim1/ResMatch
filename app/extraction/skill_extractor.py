import re
from rapidfuzz import fuzz


def load_skills(skill_file: str) -> list:
    """
    Load and normalize skills from a text file.

    Args:
        skill_file (str): Path to the skill master file.

    Returns:
        list: Sorted list of unique normalized skills.
    """
    with open(skill_file, "r", encoding="utf-8") as f:
        skills = [line.strip().lower() for line in f if line.strip()]
    return sorted(set(skills))


def normalize_text(text: str) -> str:
    """
    Normalize text for consistent skill matching.

    Args:
        text (str): Input text.

    Returns:
        str: Normalized text with cleaned separators and whitespace.
    """
    text = text.lower()
    text = re.sub(r"[\/|]", " ", text)
    text = re.sub(r"[-_]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def exact_skill_match(text: str, skill: str) -> bool:
    """
    Check for exact word-boundary match of a skill in text.

    Args:
        text (str): Normalized text.
        skill (str): Skill to match.

    Returns:
        bool: True if exact match is found, else False.
    """
    pattern = r'(?<!\w)' + re.escape(skill) + r'(?!\w)'
    return re.search(pattern, text) is not None


def extract_skills(text: str, skills_list: list, fuzzy_threshold: int = 90) -> list:
    """
    Extract skills from text using exact and fuzzy matching.

    The function first performs exact matching using word boundaries,
    followed by fuzzy matching for multi-word and approximate matches.

    Args:
        text (str): Input resume or JD text.
        skills_list (list): Master list of skills.
        fuzzy_threshold (int, optional): Threshold for fuzzy matching. Defaults to 90.

    Returns:
        list: Sorted list of detected skills.
    """
    text_norm = normalize_text(text)
    found = set()

    # Short skills are handled only via exact match to avoid false positives
    short_skills = {"c", "c++", "c#", "ai", "ml", "dl", "nlp", "rag", "sql", "aws", "gcp"}

    for skill in skills_list:
        skill_norm = normalize_text(skill)
        if exact_skill_match(text_norm, skill_norm):
            found.add(skill)

    tokens = re.findall(r'\b[a-zA-Z0-9.+#]+\b', text_norm)

    for i in range(len(tokens)):
        for j in range(i + 1, min(i + 4, len(tokens)) + 1):
            phrase = " ".join(tokens[i:j])

            for skill in skills_list:
                skill_norm = normalize_text(skill)

                if skill_norm in short_skills or len(skill_norm) < 4:
                    continue

                if abs(len(skill_norm.split()) - len(phrase.split())) > 1:
                    continue

                if fuzz.ratio(phrase, skill_norm) >= fuzzy_threshold:
                    found.add(skill)

    return sorted(found)