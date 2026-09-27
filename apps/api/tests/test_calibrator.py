from src.services.grounding.calibrator import ConfidenceCalibrator


def test_confidence_calibration_formula():
    calibrator = ConfidenceCalibrator(
        weight_retrieval=0.35,
        weight_authority=0.25,
        weight_claim=0.40
    )

    # Chunks with reranker_score = 1.0 and authority_level = 1 (weight = 1.0)
    chunks = [
        {"id": "c1", "reranker_score": 1.0, "authority_level": 1}
    ]

    # Perfect claims support (1.0), no staleness
    res = calibrator.calculate_confidence(
        retrieved_chunks=chunks,
        supported_claims_ratio=1.0,
        is_stale_topic=False
    )

    # 0.35 * 1.0 + 0.25 * 1.0 + 0.40 * 1.0 = 1.0
    assert res.composite_confidence == 1.0
    assert res.badge == "HIGHLY VERIFIED"


def test_confidence_badge_thresholds():
    calibrator = ConfidenceCalibrator()

    # Moderate retrieval score and authority
    chunks = [
        {"id": "c1", "reranker_score": 0.60, "authority_level": 2}  # auth level 2 -> 0.8
    ]

    res = calibrator.calculate_confidence(
        retrieved_chunks=chunks,
        supported_claims_ratio=0.80,
        is_stale_topic=False
    )

    # 0.35 * 0.60 + 0.25 * 0.80 + 0.40 * 0.80 = 0.21 + 0.20 + 0.32 = 0.73
    assert res.composite_confidence == 0.73
    assert res.badge == "GROUNDED"
