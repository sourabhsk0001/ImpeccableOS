from typing import List, Dict, Any, Optional
from src.services.retrieval.rrf import reciprocal_rank_fusion
from src.services.retrieval.reranker import CrossEncoderReranker
from src.services.grounding.calibrator import ConfidenceCalibrator
from src.schemas.retrieval import RetrievedChunk, HybridRetrievalResponse


class HybridRetrievalController:
    """
    Orchestrates:
    1. Dense vector similarity search (pgvector)
    2. Sparse lexical search (PostgreSQL FTS tsvector)
    3. Reciprocal Rank Fusion (k=60)
    4. Cross-Encoder reranking
    5. Confidence calibration
    """

    def __init__(self, reranker: Optional[CrossEncoderReranker] = None, calibrator: Optional[ConfidenceCalibrator] = None):
        self.reranker = reranker or CrossEncoderReranker()
        self.calibrator = calibrator or ConfidenceCalibrator()

    def fuse_and_rerank(
        self,
        query: str,
        dense_results: List[Dict[str, Any]],
        sparse_results: List[Dict[str, Any]],
        top_k: int = 5
    ) -> HybridRetrievalResponse:
        """Fuses dense and sparse candidate lists and reranks the top pool."""
        total_retrieved = len(dense_results) + len(sparse_results)
        
        # Merge via Reciprocal Rank Fusion (k=60)
        fused = reciprocal_rank_fusion([dense_results, sparse_results], k=60, top_n=20)
        
        # Cross-encoder rerank
        final_candidates = self.reranker.rerank(query=query, candidates=fused, top_n=top_k)
        
        # Calculate confidence breakdown
        confidence = self.calibrator.calculate_confidence(
            retrieved_chunks=final_candidates,
            supported_claims_ratio=1.0,
            is_stale_topic=False
        )

        chunk_schemas = [
            RetrievedChunk(
                id=c["id"],
                source_title=c.get("source_title", "Technical Documentation"),
                section_title=c.get("section_title"),
                domain_topic=c.get("domain_topic", "General"),
                content=c.get("content", ""),
                authority_level=c.get("authority_level", 1),
                source_url=c.get("source_url"),
                dense_score=c.get("dense_score"),
                sparse_score=c.get("sparse_score"),
                rrf_score=c.get("rrf_score"),
                reranker_score=c.get("reranker_score")
            )
            for c in final_candidates
        ]

        return HybridRetrievalResponse(
            query=query,
            total_candidates_retrieved=total_retrieved,
            fused_candidates_count=len(fused),
            final_chunks=chunk_schemas,
            web_fallback_triggered=False,
            confidence_metrics=confidence
        )
