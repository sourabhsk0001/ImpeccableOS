import re
from typing import List, Dict, Any, Tuple


class FreshnessGatingClassifier:
    """
    Implements deterministic gating for live web research:
    Prevents unnecessary search latency and API burn on stable foundational concepts.
    """

    TEMPORAL_KEYWORDS = [
        r"\blatest\b",
        r"\bcurrent version\b",
        r"\brelease notes\b",
        r"\bnewest\b",
        r"\bchangelog\b",
        r"\bbreaking changes\b",
        r"\bdeprecated\b",
        r"\bv[0-9]+\.[0-9]+\b",
        r"\b2025\b",
        r"\b2026\b"
    ]

    EVOLVING_TOPICS = [
        "mcp",
        "model context protocol",
        "langgraph",
        "vllm",
        "reasoning model",
        "claude 3.5",
        "gpt-4o",
        "deepseek",
        "pydantic ai",
        "agent protocol"
    ]

    def __init__(self, fallback_threshold: float = 0.50):
        self.fallback_threshold = fallback_threshold
        self.temporal_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in self.TEMPORAL_KEYWORDS
        ]

    def has_temporal_keywords(self, query: str) -> bool:
        """Checks if the query explicitly asks for recent/versioned facts."""
        for pattern in self.temporal_patterns:
            if pattern.search(query):
                return True
        return False

    def is_evolving_topic(self, query: str) -> bool:
        """Determines if the topic belongs to rapidly evolving modern AI infrastructure."""
        q_lower = query.lower()
        return any(topic in q_lower for topic in self.EVOLVING_TOPICS)

    def should_trigger_web_research(
        self,
        query: str,
        top_chunks: List[Dict[str, Any]],
        force_research: bool = False
    ) -> Tuple[bool, str]:
        """
        Evaluates whether live web research must be dispatched.
        Returns: (should_trigger, reason_code)
        """
        if force_research:
            return True, "FORCED_BY_USER"

        # Rule 1: Explicit temporal/version query
        if self.has_temporal_keywords(query):
            return True, "TEMPORAL_RECENCY_KEYWORD_DETECTED"

        # Rule 2: Evolving topic + Static RAG relevance score fallback below threshold
        if self.is_evolving_topic(query):
            if not top_chunks:
                return True, "EVOLVING_TOPIC_NO_STATIC_CHUNKS"
            
            max_relevance = max(c.get("reranker_score", 0.0) for c in top_chunks)
            if max_relevance < self.fallback_threshold:
                return True, f"EVOLVING_TOPIC_LOW_CONFIDENCE_{max_relevance:.2f}"

        # Stable foundational concept: Static RAG is sufficient
        return False, "STATIC_RAG_SUFFICIENT"
