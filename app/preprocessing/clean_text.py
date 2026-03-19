import re

ABBREVIATION_MAP = {
    "ml": "machine learning",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "ai": "artificial intelligence"
}


def normalize_abbreviations(text: str) -> str:
    words = text.split()
    normalized = []

    for word in words:
        cleaned = re.sub(r"[^\w\s]", "", word.lower())
        normalized.append(ABBREVIATION_MAP.get(cleaned, word))

    return " ".join(normalized)


def clean_text(text: str) -> str:
    text = text.lower()
    text = normalize_abbreviations(text)
    text = re.sub(r"\r", " ", text)
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[^\w\s\+\#\.\-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_summary_text(text: str) -> str:
    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # remove phone numbers
        if re.search(r'\+?\d[\d\s\-]{8,}', line):
            continue

        # remove emails
        if "@" in line:
            continue

        # remove links
        if "linkedin" in line.lower() or "github" in line.lower():
            continue

        # remove headers
        if line.lower() in ["professional summary", "summary"]:
            continue

        # remove uppercase name lines
        if line.isupper() and len(line.split()) <= 5:
            continue

        cleaned_lines.append(line)

    return " ".join(cleaned_lines)