def education_score(jd_education: list, resume_education: list) -> float:
    if not jd_education:
        return 1.0

    jd_set = set(e.strip().lower() for e in jd_education)
    resume_set = set(e.strip().lower() for e in resume_education)

    
    if jd_set & resume_set:
        return 1.0

    related_fields = {
        "cybersecurity", "cyber security",
        "computer science", "computer engineering",
        "information technology", "information systems", "it",
        "computer applications", "bca", "mca",
        "data science", "data analytics", "analytics",
        "machine learning", "artificial intelligence", "ai", "ml", "ai/ml",
        "cloud computing",
        "software engineering",
        "robotics"
    }

    if (jd_set & related_fields) and (resume_set & related_fields):
        return 1.0

    return 0.0

def experience_score(jd_exp: int, resume_exp: int) -> float:
    if jd_exp == 0:
        return 1.0
    if resume_exp >= jd_exp:
        return 1.0
    return round(resume_exp / jd_exp, 2)


def final_score(skill_score, semantic_score, exp_score, edu_score):
    return round(
        0.40 * skill_score +
        0.35 * semantic_score +
        0.15 * exp_score +
        0.10 * edu_score,
        4
    )


def classify_candidate(score: float) -> str:
    if score >= 0.75:
        return "Highly Suitable"
    elif score >= 0.55:
        return "Moderately Suitable"
    return "Not Suitable"