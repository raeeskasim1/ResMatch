def build_explanation(jd_data: dict, resume_data: dict) -> dict:
    matched_skills = sorted(set(jd_data["skills"]).intersection(set(resume_data["skills"])))
    missing_skills = sorted(set(jd_data["skills"]) - set(resume_data["skills"]))

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "experience_gap": f'JD asks {jd_data["experience"]} years, candidate has {resume_data["experience"]} years',
        "education_match": "Matched" if set(jd_data["education"]).intersection(set(resume_data["education"])) else "Not matched"
    }