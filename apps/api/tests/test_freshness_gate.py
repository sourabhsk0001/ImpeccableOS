import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.research.freshness import FreshnessGatingClassifier


class TestFreshnessGate(unittest.TestCase):

    def test_freshness_gate_temporal_keywords(self):
        gate = FreshnessGatingClassifier(fallback_threshold=0.50)

        should_search, reason = gate.should_trigger_web_research(
            query="What are the latest breaking changes in LangGraph v0.2?",
            top_chunks=[]
        )
        self.assertTrue(should_search)
        self.assertIn("TEMPORAL_RECENCY", reason)

    def test_freshness_gate_stable_topic(self):
        gate = FreshnessGatingClassifier(fallback_threshold=0.50)

        should_search, reason = gate.should_trigger_web_research(
            query="How does dot-product attention compute softmax scaling?",
            top_chunks=[{"reranker_score": 0.88}]
        )
        self.assertFalse(should_search)
        self.assertEqual(reason, "STATIC_RAG_SUFFICIENT")

    def test_freshness_gate_evolving_fallback(self):
        gate = FreshnessGatingClassifier(fallback_threshold=0.50)

        should_search, reason = gate.should_trigger_web_research(
            query="How does Model Context Protocol handle roots and resources?",
            top_chunks=[{"reranker_score": 0.35}]
        )
        self.assertTrue(should_search)
        self.assertIn("EVOLVING_TOPIC_LOW_CONFIDENCE", reason)


if __name__ == "__main__":
    unittest.main()
