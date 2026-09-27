import unittest
import sys
import os

# Add apps/api to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.dag.engine import DAGEngine
from src.services.retrieval.rrf import reciprocal_rank_fusion
from src.services.research.freshness import FreshnessGatingClassifier


class TestCoreAlgorithms(unittest.TestCase):

    def test_dag_cycle_detection(self):
        engine = DAGEngine()
        engine.add_skill("a", "Skill A", "test")
        engine.add_skill("b", "Skill B", "test")
        engine.add_prerequisite("a", "b")
        with self.assertRaises(ValueError):
            engine.add_prerequisite("b", "a")

    def test_ema_mastery(self):
        engine = DAGEngine(alpha=0.30)
        m1 = engine.calculate_ema_mastery(0.0, 0.80)
        self.assertEqual(m1, 0.80)

        m2 = engine.calculate_ema_mastery(m1, 0.90)
        self.assertEqual(m2, 0.83)

        m3 = engine.calculate_ema_mastery(m2, 0.40)
        self.assertEqual(m3, 0.701)

    def test_topological_sort(self):
        engine = DAGEngine()
        engine.add_skill("math", "Math", "ai")
        engine.add_skill("transformers", "Transformers", "ai")
        engine.add_skill("agents", "Agents", "ai")
        engine.add_prerequisite("math", "transformers")
        engine.add_prerequisite("transformers", "agents")

        roadmap = engine.generate_topological_roadmap("agents")
        self.assertEqual(roadmap, ["math", "transformers", "agents"])

    def test_rrf_scoring(self):
        dense = [{"id": "doc1", "content": "A"}, {"id": "doc2", "content": "B"}]
        sparse = [{"id": "doc2", "content": "B"}, {"id": "doc3", "content": "C"}]
        fused = reciprocal_rank_fusion([dense, sparse], k=60, top_n=3)
        self.assertEqual(len(fused), 3)
        self.assertEqual(fused[0]["id"], "doc2")
        self.assertGreater(fused[0]["rrf_score"], fused[1]["rrf_score"])

    def test_freshness_gating(self):
        gate = FreshnessGatingClassifier(fallback_threshold=0.50)
        should_web, reason = gate.should_trigger_web_research(
            "What are the latest breaking changes in v0.2?", []
        )
        self.assertTrue(should_web)

        should_web2, _ = gate.should_trigger_web_research(
            "Explain dot product attention", [{"reranker_score": 0.9}]
        )
        self.assertFalse(should_web2)


if __name__ == "__main__":
    unittest.main()
