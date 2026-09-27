from fastapi import APIRouter
from src.schemas.retrieval import RetrievalQuery, HybridRetrievalResponse
from src.services.retrieval.hybrid import HybridRetrievalController
from src.services.research.freshness import FreshnessGatingClassifier

router = APIRouter()
controller = HybridRetrievalController()
freshness_gate = FreshnessGatingClassifier()


@router.post("/search", response_model=HybridRetrievalResponse, tags=["Retrieval"])
async def hybrid_search(query: RetrievalQuery):
    """
    Executes dense pgvector + sparse FTS query fusion via RRF and reranks with cross-encoder.
    """
    # Sample corpus representation for fast in-memory execution / demo
    mock_dense_results = [
        {
            "id": "doc-rag-01",
            "source_title": "Reciprocal Rank Fusion in Production RAG",
            "section_title": "RRF Parameter Tuning (k=60)",
            "domain_topic": "rag_systems",
            "content": "Reciprocal Rank Fusion combines ordinal ranks from dense vector search and sparse BM25/FTS without needing cross-distribution score normalization.",
            "authority_level": 1,
            "dense_score": 0.89
        },
        {
            "id": "doc-rag-02",
            "source_title": "PostgreSQL Full-Text Search vs pgvector",
            "section_title": "Hybrid Query Planning",
            "domain_topic": "rag_systems",
            "content": "PostgreSQL 16 allows executing tsvector text search and pgvector cosine distance <=> queries within a single relational ACID transaction.",
            "authority_level": 1,
            "dense_score": 0.84
        }
    ]

    mock_sparse_results = [
        {
            "id": "doc-rag-02",
            "source_title": "PostgreSQL Full-Text Search vs pgvector",
            "section_title": "Hybrid Query Planning",
            "domain_topic": "rag_systems",
            "content": "PostgreSQL 16 allows executing tsvector text search and pgvector cosine distance <=> queries within a single relational ACID transaction.",
            "authority_level": 1,
            "sparse_score": 0.92
        },
        {
            "id": "doc-agent-01",
            "source_title": "Deterministic State Machines for AI Agents",
            "section_title": "State Loops & Transition Rules",
            "domain_topic": "agent_systems",
            "content": "Decouple LLM probabilistic semantic parsing from deterministic mathematical state transitions to eliminate prompt injection vulnerabilities.",
            "authority_level": 2,
            "sparse_score": 0.79
        }
    ]

    should_web_search, reason = freshness_gate.should_trigger_web_research(
        query=query.query,
        top_chunks=mock_dense_results,
        force_research=query.force_web_search
    )

    response = controller.fuse_and_rerank(
        query=query.query,
        dense_results=mock_dense_results,
        sparse_results=mock_sparse_results,
        top_k=query.top_k
    )
    response.web_fallback_triggered = should_web_search

    return response
