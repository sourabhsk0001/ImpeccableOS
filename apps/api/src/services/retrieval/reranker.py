from typing import List, Dict, Any, Optional
import math


class CrossEncoderReranker:
    """
    Reranks candidate chunks using cross-encoder relevance modeling.
    Supports FlashRank ONNX runtime when available, with deterministic semantic lexical scoring fallback.
    """

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self.ranker = None
        self._init_ranker()

    def _init_ranker(self):
        try:
            from flashrank import Ranker
            self.ranker = Ranker(model_name=self.model_name, cache_dir="/tmp/flashrank")
        except Exception:
            # Fallback to internal scoring if flashrank weight files are not locally downloaded
            self.ranker = None

    def rerank(self, query: str, candidates: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Reranks candidates against the query and attaches normalized reranker_score.
        """
        if not candidates:
            return []

        if self.ranker:
            try:
                passages = [
                    {"id": c["id"], "text": c["content"], "meta": c}
                    for c in candidates
                ]
                from flashrank import RerankRequest
                request = RerankRequest(query=query, passages=passages)
                results = self.ranker.rerank(request)
                
                reranked_docs = []
                for item in results[:top_n]:
                    doc = item["meta"]
                    # FlashRank score is typically between 0.0 and 1.0
                    doc["reranker_score"] = round(float(item["score"]), 4)
                    reranked_docs.append(doc)
                return reranked_docs
            except Exception:
                pass

        # Robust heuristic fallback: Term overlap + density + authority weighting
        query_terms = set(query.lower().split())
        scored_candidates = []

        for candidate in candidates:
            content_lower = candidate.get("content", "").lower()
            source_lower = candidate.get("source_title", "").lower()
            
            # Exact matches count higher
            overlap_count = sum(1 for term in query_terms if term in content_lower)
            title_overlap = sum(2 for term in query_terms if term in source_lower)
            
            # Baseline from RRF score if present
            base_rrf = candidate.get("rrf_score", 0.01) * 20.0
            term_score = (overlap_count + title_overlap) / max(1, len(query_terms))
            
            # Normalization into [0.0, 1.0] sigmoid
            raw_val = (term_score * 0.7) + (base_rrf * 0.3)
            normalized_score = round(1.0 / (1.0 + math.exp(-3.0 * (raw_val - 0.5))), 4)
            
            candidate_copy = dict(candidate)
            candidate_copy["reranker_score"] = normalized_score
            scored_candidates.append(candidate_copy)

        scored_candidates.sort(key=lambda x: x["reranker_score"], reverse=True)
        return scored_candidates[:top_n]
