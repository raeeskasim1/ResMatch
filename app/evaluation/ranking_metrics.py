import math
from typing import List, Dict


def reciprocal_rank(binary_relevance: List[int]) -> float:
    """
    Compute reciprocal rank for a single ranked result list.

    Args:
        binary_relevance (List[int]): Ranked binary relevance labels where
            1 indicates relevant and 0 indicates non-relevant.

    Returns:
        float: Reciprocal rank score for the first relevant item.
    """
    for rank, rel in enumerate(binary_relevance, start=1):
        if rel == 1:
            return 1.0 / rank
    return 0.0


def mean_reciprocal_rank(all_binary_rankings: List[List[int]]) -> float:
    """
    Compute mean reciprocal rank across multiple ranked result lists.

    Args:
        all_binary_rankings (List[List[int]]): List of ranked binary relevance lists.

    Returns:
        float: Mean reciprocal rank.
    """
    if not all_binary_rankings:
        return 0.0
    rr_scores = [reciprocal_rank(ranking) for ranking in all_binary_rankings]
    return sum(rr_scores) / len(rr_scores)


def dcg(relevance_scores: List[int], k: int = None) -> float:
    """
    Compute Discounted Cumulative Gain (DCG) for a ranked relevance list.

    Args:
        relevance_scores (List[int]): Ranked graded relevance scores.
        k (int, optional): Number of top items to consider.

    Returns:
        float: DCG score.
    """
    if k is not None:
        relevance_scores = relevance_scores[:k]

    score = 0.0
    for i, rel in enumerate(relevance_scores, start=1):
        score += rel / math.log2(i + 1)
    return score


def ndcg(relevance_scores: List[int], k: int = None) -> float:
    """
    Compute Normalized Discounted Cumulative Gain (NDCG) for a ranked relevance list.

    Args:
        relevance_scores (List[int]): Ranked graded relevance scores.
        k (int, optional): Number of top items to consider.

    Returns:
        float: NDCG score.
    """
    if not relevance_scores:
        return 0.0

    actual_dcg = dcg(relevance_scores, k)
    ideal_dcg = dcg(sorted(relevance_scores, reverse=True), k)

    if ideal_dcg == 0:
        return 0.0

    return actual_dcg / ideal_dcg


def mean_ndcg(all_graded_rankings: List[List[int]], k: int = None) -> float:
    """
    Compute mean NDCG across multiple ranked result lists.

    Args:
        all_graded_rankings (List[List[int]]): List of ranked graded relevance lists.
        k (int, optional): Number of top items to consider.

    Returns:
        float: Mean NDCG score.
    """
    if not all_graded_rankings:
        return 0.0
    ndcg_scores = [ndcg(ranking, k) for ranking in all_graded_rankings]
    return sum(ndcg_scores) / len(ndcg_scores)


def evaluate_single_jd(ranked_results: List[Dict]) -> Dict[str, float]:
    """
    Evaluate ranking metrics for a single job description.

    Args:
        ranked_results (List[Dict]): Ranked candidate results containing
            true_relevance values.

    Returns:
        Dict[str, float]: Ranking evaluation metrics including MRR, NDCG,
        NDCG@5, and NDCG@10.
    """
    if not ranked_results:
        return {
            "MRR": 0.0,
            "NDCG": 0.0,
            "NDCG@5": 0.0,
            "NDCG@10": 0.0,
        }

    graded = [item["true_relevance"] for item in ranked_results]
    binary = [1 if rel > 0 else 0 for rel in graded]

    return {
        "MRR": reciprocal_rank(binary),
        "NDCG": ndcg(graded),
        "NDCG@5": ndcg(graded, k=5),
        "NDCG@10": ndcg(graded, k=10),
    }


def evaluate_multiple_jds(all_ranked_results: List[List[Dict]]) -> Dict[str, float]:
    """
    Evaluate average ranking metrics across multiple job descriptions.

    Args:
        all_ranked_results (List[List[Dict]]): List of ranked candidate results
            for multiple job descriptions.

    Returns:
        Dict[str, float]: Mean ranking metrics including Mean MRR, Mean NDCG,
        Mean NDCG@5, and Mean NDCG@10.
    """
    if not all_ranked_results:
        return {
            "Mean MRR": 0.0,
            "Mean NDCG": 0.0,
            "Mean NDCG@5": 0.0,
            "Mean NDCG@10": 0.0,
        }

    all_binary_rankings = []
    all_graded_rankings = []

    for ranked_results in all_ranked_results:
        graded = [item["true_relevance"] for item in ranked_results]
        binary = [1 if rel > 0 else 0 for rel in graded]

        all_binary_rankings.append(binary)
        all_graded_rankings.append(graded)

    return {
        "Mean MRR": mean_reciprocal_rank(all_binary_rankings),
        "Mean NDCG": mean_ndcg(all_graded_rankings),
        "Mean NDCG@5": mean_ndcg(all_graded_rankings, k=5),
        "Mean NDCG@10": mean_ndcg(all_graded_rankings, k=10),
    }