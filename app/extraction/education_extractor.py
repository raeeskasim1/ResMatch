import re

DEGREE_KEYWORDS = [
    "b.tech", "btech", "b.e", "be", "bsc", "b.sc", "bca",
    "m.tech", "mtech", "m.e", "msc", "m.sc", "mca",
    "bachelor", "master", "phd", "doctorate", "diploma"
]

FIELD_KEYWORDS = [
    "cybersecurity", "cyber security",
    "computer science", "computer engineering",
    "information technology", "information systems", "it",
    "computer applications",
    "data science", "data analytics", "analytics",
    "machine learning", "artificial intelligence", "ai", "ml", "ai/ml",
    "cloud computing",
    "software engineering",
    "robotics"
]


def extract_education(text: str) -> list:
    text = text.lower()
    found = set()

    for keyword in DEGREE_KEYWORDS:
        if re.search(r"\b" + re.escape(keyword) + r"\b", text):
            found.add(keyword)

    for keyword in FIELD_KEYWORDS:
        if re.search(r"\b" + re.escape(keyword) + r"\b", text):
            found.add(keyword)

    return sorted(found)