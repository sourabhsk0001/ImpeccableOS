from typing import List, Dict, Any


def reciprocal_rank_fusion(
    ranked_lists: List[List[Dict[str, Any]]],
    k: int = 60,
    top_n: int = 20
) -> List[Dict[str, Any]]:
    """
    Combines multiple ranked lists using Reciprocal Rank Fusion (RRF):
    RRF_score(d) = sum_{m in M} 1 / (k + rank_m(d))
    
    Args:
        ranked_lists: List of ranked item lists (each item is a dict with an 'id' key).
        k: Smoothing constant (default: 60 as per standard IR benchmarks and ADR 003).
        top_n: Max fused items to return.
    """
    scores: Dict[str, float] = {}
    doc_registry: Dict[str, Dict[str, Any]] = {}

    for ranked_list in ranked_lists:
        for rank, item in enumerate(ranked_list, start=1):
            doc_id = str(item.get("id"))
            if doc_id not in scores:
                scores[doc_id] = 0.0
                doc_registry[doc_id] = dict(item)
            
            scores[doc_id] += 1.0 / (k + rank)
            # Retain any specific score keys from ranking models
            if "dense_score" in item:
                doc_registry[doc_id]["dense_score"] = item["dense_score"]
            if "sparse_score" in item:
                doc_registry[doc_id]["sparse_score"] = item["sparse_score"]

    # Sort documents descending by fused RRF score
    sorted_doc_ids = sorted(scores.keys(), key=lambda d: scores[d], reverse=True)

    fused_results = []
    for doc_id in sorted_doc_ids[:top_n]:
        doc = doc_registry[doc_id]
        doc["rrf_score"] = round(scores[doc_id], 6)
        fused_results.append(doc)

    return fused_results
