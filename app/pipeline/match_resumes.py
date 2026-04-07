import uuid
from app.extraction.skill_extractor import load_skills
from app.embeddings.embedder import TextEmbedder
from app.vectordb.resume_store import query_resumes
from app.vectordb.jd_store import add_jd
from app.pipeline.process_jd import process_jd
from app.scoring.similarity import compute_cosine_similarity, skill_overlap_score
from app.scoring.reranker import education_score, experience_score, final_score, classify_candidate
from app.scoring.explainability import build_explanation

SKILL_FILE = "data/skills_master.txt"


def search_and_rank(jd_text: str, top_k: int = 5):
    """
    Match a job description against indexed resumes and return ranked candidates.

    This function processes the job description, generates its embedding, stores it
    in the job description vector store, retrieves the most relevant resumes, and
    computes candidate ranking scores based on semantic similarity, skill overlap,
    experience match, and education match.

    Args:
        jd_text (str): Job description text entered by the user.
        top_k (int, optional): Number of top resumes to retrieve. Defaults to 5.

    Returns:
        list: Ranked list of candidate results with scoring details, decision label,
        explanation, and resume preview.
    """
    skills_list = load_skills(SKILL_FILE)
    embedder = TextEmbedder()

    jd_data = process_jd(jd_text, skills_list)
    jd_embedding = embedder.encode_one(jd_data["cleaned_text"])

    jd_id = str(uuid.uuid4())
    add_jd(
        jd_id=jd_id,
        document=jd_data["cleaned_text"],
        embedding=jd_embedding,
        metadata={"skills": ",".join(jd_data["skills"])}
    )

    retrieve_k = max(20, top_k)
    results = query_resumes(jd_embedding, top_k=retrieve_k)

    ranked = []
    ids = results["ids"][0]
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]
    embeddings = results["embeddings"][0]

    for i, (idx, doc, meta, dist) in enumerate(zip(ids, docs, metas, distances)):
        resume_skills = meta.get("skills", "").split(",") if meta.get("skills") else []
        resume_education = meta.get("education", "").split(",") if meta.get("education") else []
        resume_exp = int(float(meta.get("experience_years", 0) or 0))

        skill_score = skill_overlap_score(jd_data["skills"], resume_skills)
        semantic_score = compute_cosine_similarity(jd_embedding, embeddings[i])
        exp_score = experience_score(jd_data["experience"], resume_exp)
        edu_score = education_score(jd_data["education"], resume_education)

        score = final_score(skill_score, semantic_score, exp_score, edu_score)
        decision = classify_candidate(score)

        resume_data = {
            "skills": resume_skills,
            "education": resume_education,
            "experience": resume_exp
        }

        explanation = build_explanation(jd_data, resume_data)

        ranked.append({
            "resume_id": idx,
            "candidate_name": meta.get("candidate_name", "Unknown"),
            "file_name": meta.get("file_name", ""),
            "db_distance": round(float(dist), 4),
            "semantic_score": round(semantic_score, 4),
            "skill_score": round(skill_score, 4),
            "experience_score": round(exp_score, 4),
            "education_score": round(edu_score, 4),
            "final_score": score,
            "decision": decision,
            "explanation": explanation,
            "resume_preview": meta.get("summary", "").strip() or doc[:600]
        })

    ranked.sort(key=lambda x: x["final_score"], reverse=True)
    return ranked[:top_k]
