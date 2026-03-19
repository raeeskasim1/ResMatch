from typing import List, Dict


def analyze_similarity_distribution(results: List[Dict]) -> Dict:
    matched_scores = []
    unmatched_scores = []

    for r in results:
        score = r.get("semantic_score", 0.0)
        decision = r.get("decision", "")

        if decision in ["Highly Suitable", "Moderately Suitable"]:
            matched_scores.append(score)
        else:
            unmatched_scores.append(score)

    matched_avg = sum(matched_scores) / len(matched_scores) if matched_scores else 0.0
    unmatched_avg = sum(unmatched_scores) / len(unmatched_scores) if unmatched_scores else 0.0

    return {
        "matched_scores": matched_scores,
        "unmatched_scores": unmatched_scores,
        "matched_avg": matched_avg,
        "unmatched_avg": unmatched_avg,
    }