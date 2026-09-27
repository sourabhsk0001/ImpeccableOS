from typing import List, Dict, Any, Tuple
from src.schemas.retrieval import ConfidenceBreakdown


class ConfidenceCalibrator:
    """
    Computes deterministic confidence calibration from objective evidence properties:
    Confidence = 0.35 * S_retrieval + 0.25 * S_authority + 0.40 * S_claim_support - P_staleness
    """

    AUTHORITY_WEIGHTS: Dict[int, float] = {
        1: 1.00,  # Tier 1: Official Specifications, Framework Documentation, RFCs
        2: 0.80,  # Tier 2: Core Maintainer Engineering Blogs, Verified Benchmarks
        3: 0.50,  # Tier 3: Third-Party Community Tutorials & Articles
    }

    def __init__(
        self,
        weight_retrieval: float = 0.35,
        weight_authority: float = 0.25,
        weight_claim: float = 0.40,
        default_staleness_penalty: float = 0.00
    ):
        self.w_ret = weight_retrieval
        self.w_auth = weight_authority
        self.w_claim = weight_claim
        self.p_stale = default_staleness_penalty

    def calculate_confidence(
        self,
        retrieved_chunks: List[Dict[str, Any]],
        supported_claims_ratio: float = 1.0,
        is_stale_topic: bool = False
    ) -> ConfidenceBreakdown:
        """
        Computes composite confidence and categorizes the audit badge.
        """
        # 1. Retrieval Relevance Score (mean reranker_score of top chunks)
        if retrieved_chunks:
            reranker_scores = [c.get("reranker_score", 0.50) for c in retrieved_chunks]
            s_retrieval = sum(reranker_scores) / len(reranker_scores)
        else:
            s_retrieval = 0.0

        # 2. Source Authority Score (mean mapped authority weight)
        if retrieved_chunks:
            auth_levels = [c.get("authority_level", 2) for c in retrieved_chunks]
            mapped_auth = [self.AUTHORITY_WEIGHTS.get(lvl, 0.50) for lvl in auth_levels]
            s_authority = sum(mapped_auth) / len(mapped_auth)
        else:
            s_authority = 0.0

        # 3. Claim Support Score (ratio of assertions with grounded chunk quotes)
        s_claim = max(0.0, min(1.0, supported_claims_ratio))

        # 4. Staleness Penalty
        staleness_penalty = 0.10 if is_stale_topic else 0.0

        # Formula calculation
        raw_composite = (
            (self.w_ret * s_retrieval) +
            (self.w_auth * s_authority) +
            (self.w_claim * s_claim) -
            staleness_penalty
        )
        composite = round(max(0.0, min(1.0, raw_composite)), 4)

        # Categorical Badge Assignment
        if composite >= 0.85:
            badge = "HIGHLY VERIFIED"
        elif composite >= 0.70:
            badge = "GROUNDED"
        elif composite >= 0.50:
            badge = "PROBABILISTIC"
        else:
            badge = "LOW CONFIDENCE"

        return ConfidenceBreakdown(
            composite_confidence=composite,
            retrieval_relevance=round(s_retrieval, 4),
            source_authority=round(s_authority, 4),
            claim_support=round(s_claim, 4),
            staleness_penalty=round(staleness_penalty, 4),
            badge=badge
        )
