from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class RetrievalQuery(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=20)
    domain_filter: Optional[str] = None
    force_web_search: bool = False


class RetrievedChunk(BaseModel):
    id: str
    source_title: str
    section_title: Optional[str] = None
    domain_topic: str
    content: str
    authority_level: int
    source_url: Optional[str] = None
    dense_score: Optional[float] = None
    sparse_score: Optional[float] = None
    rrf_score: Optional[float] = None
    reranker_score: Optional[float] = None


class ConfidenceBreakdown(BaseModel):
    composite_confidence: float
    retrieval_relevance: float
    source_authority: float
    claim_support: float
    staleness_penalty: float
    badge: str  # "HIGHLY VERIFIED", "GROUNDED", "PROBABILISTIC", "LOW CONFIDENCE"


class HybridRetrievalResponse(BaseModel):
    query: str
    total_candidates_retrieved: int
    fused_candidates_count: int
    final_chunks: List[RetrievedChunk]
    web_fallback_triggered: bool
    confidence_metrics: Optional[ConfidenceBreakdown] = None
