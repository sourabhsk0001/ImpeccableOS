import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.retrieval.rrf import reciprocal_rank_fusion


class TestRRF(unittest.TestCase):

    def test_rrf_scoring_and_ranking(self):
        dense = [{"id": "doc1", "content": "dense top"}, {"id": "doc2", "content": "dense second"}]
        sparse = [{"id": "doc2", "content": "sparse top"}, {"id": "doc3", "content": "sparse second"}]

        fused = reciprocal_rank_fusion([dense, sparse], k=60, top_n=3)

        self.assertEqual(len(fused), 3)
        self.assertEqual(fused[0]["id"], "doc2")
        self.assertEqual(fused[1]["id"], "doc1")
        self.assertEqual(fused[2]["id"], "doc3")
        self.assertGreater(fused[0]["rrf_score"], fused[1]["rrf_score"])


if __name__ == "__main__":
    unittest.main()
