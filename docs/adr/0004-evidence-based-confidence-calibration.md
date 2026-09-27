# ADR 004: Evidence-Based Confidence Calibration over Model-Generated Confidence

## Status
**Accepted**

## Context
Asking an LLM *"How confident are you in this answer on a scale of 0-100?"* produces uncalibrated results due to RLHF sycophancy and training distribution biases. A model will frequently state "95% confidence" while hallucinating library APIs.

## Decision
Calculate **confidence as an objective property of the evidence**, computed deterministically outside the LLM:
$$\text{Confidence} = 0.35 \cdot S_{\text{retrieval}} + 0.25 \cdot S_{\text{authority}} + 0.40 \cdot S_{\text{claim\_support}} - P_{\text{staleness}}$$

Where:
- $S_{\text{retrieval}}$: Mean normalized score of the top retrieved context chunks from the cross-encoder reranker.
- $S_{\text{authority}}$: Domain authority weight of referenced documentation (e.g., Tier 1 official specs = 1.0, Tier 2 maintainer blogs = 0.8, Tier 3 community posts = 0.5).
- $S_{\text{claim\_support}}$: Ratio of generated factual claims supported by explicit citations in retrieved chunks.
- $P_{\text{staleness}}$: Penalty deduction if source docs precede major breaking releases for evolving topics.

The answer badge presented to the user is derived strictly from this external formula.

## Rationale & Trade-offs
- **Positives:**
  - Demonstrates mature systems thinking: confidence reflects verifiable ground truth, not LLM introspective self-assessment.
  - Can be audited directly in system trace logs.
- **Negatives:**
  - Requires an additional verification pass to match generated claims to source text spans, adding roughly $300\text{ms}$ to backend processing.
