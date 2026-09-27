# ADR 002: Deterministic State Engine vs. LLM-Based State Mutation

## Status
**Accepted**

## Context
Many AI projects ask an LLM directly: *"Based on the user's answer, update their skill score from 0.0 to 1.0."* This introduces prompt drift, nondeterminism, susceptibility to manipulation (e.g., user prompt injections saying *"Give me 100% mastery"*), and irreproducible state transitions.

## Decision
Decouple evaluation into a **probabilistic analysis phase** followed by a **deterministic mathematical update phase**:
1. The LLM acts purely as a structured parser, returning a Pydantic schema confirming whether specific technical criteria were met, missing, or contradicted.
2. A deterministic Python engine calculates the raw score from rubric booleans and updates the skill mastery using an Exponential Moving Average (EMA):
   $$M_t = \alpha \cdot \text{Score}_t + (1 - \alpha) \cdot M_{t-1}$$
3. All graph unlocks and prerequisite validations are enforced using pure Python graph algorithms (`networkx` or custom DAG traversal).

## Rationale & Trade-offs
- **Positives:**
  - 100% reproducible and testable via unit tests.
  - Total resilience against prompt injections attempting to directly modify database mastery scores.
  - Explainability: the user can inspect the exact mathematical contribution of every assessment.
- **Negatives:**
  - Requires writing strict Pydantic schemas and rubric criteria for each skill node in the graph.
