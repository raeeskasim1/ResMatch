from sklearn.metrics.pairwise import cosine_similarity


def compute_cosine_similarity(vec1, vec2) -> float:
    return float(cosine_similarity([vec1], [vec2])[0][0])


def skill_overlap_score(jd_skills: list, resume_skills: list) -> float:
    if not jd_skills:
        return 0.0

    jd_set = set(jd_skills)
    resume_set = set(resume_skills)

    return len(jd_set.intersection(resume_set)) / len(jd_set)