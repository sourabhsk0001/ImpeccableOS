from src.services.research.freshness import FreshnessGatingClassifier


def test_freshness_gate_temporal_keywords():
    gate = FreshnessGatingClassifier(fallback_threshold=0.50)

    # Query with 'latest' keyword
    should_search, reason = gate.should_trigger_web_research(
        query="What are the latest breaking changes in LangGraph v0.2?",
        top_chunks=[]
    )
    assert should_search is True
    assert "TEMPORAL_RECENCY" in reason


def test_freshness_gate_stable_topic():
    gate = FreshnessGatingClassifier(fallback_threshold=0.50)

    # Foundational math concept
    should_search, reason = gate.should_trigger_web_research(
        query="How does dot-product attention compute softmax scaling?",
        top_chunks=[{"reranker_score": 0.88}]
    )
    assert should_search is False
    assert reason == "STATIC_RAG_SUFFICIENT"


def test_freshness_gate_evolving_fallback():
    gate = FreshnessGatingClassifier(fallback_threshold=0.50)

    # Evolving topic with low reranker score in static RAG
    should_search, reason = gate.should_trigger_web_research(
        query="How does Model Context Protocol handle roots and resources?",
        top_chunks=[{"reranker_score": 0.35}]
    )
    assert should_search is True
    assert "EVOLVING_TOPIC_LOW_CONFIDENCE" in reason
