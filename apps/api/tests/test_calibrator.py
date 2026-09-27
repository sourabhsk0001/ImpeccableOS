import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.grounding.calibrator import ConfidenceCalibrator


class TestCalibrator(unittest.TestCase):

    def test_confidence_calibration_formula(self):
        calibrator = ConfidenceCalibrator(
            weight_retrieval=0.35,
            weight_authority=0.25,
            weight_claim=0.40
        )

        chunks = [
            {"id": "c1", "reranker_score": 1.0, "authority_level": 1}
        ]

        res = calibrator.calculate_confidence(
            retrieved_chunks=chunks,
            supported_claims_ratio=1.0,
            is_stale_topic=False
        )

        self.assertEqual(res.composite_confidence, 1.0)
        self.assertEqual(res.badge, "HIGHLY VERIFIED")

    def test_confidence_badge_thresholds(self):
        calibrator = ConfidenceCalibrator()

        chunks = [
            {"id": "c1", "reranker_score": 0.60, "authority_level": 2}
        ]

        res = calibrator.calculate_confidence(
            retrieved_chunks=chunks,
            supported_claims_ratio=0.80,
            is_stale_topic=False
        )

        self.assertEqual(res.composite_confidence, 0.73)
        self.assertEqual(res.badge, "GROUNDED")


if __name__ == "__main__":
    unittest.main()
