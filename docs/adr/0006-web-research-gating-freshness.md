# ADR 006: Web Research Gating via Freshness & Fallback Triggers

## Status
**Accepted**

## Context
Triggering live web search on every user prompt drastically increases latency (8s+), introduces API cost, and exposes the model to prompt injections or SEO spam from arbitrary websites.

## Decision
Route queries through a **deterministic Freshness Gating rule**:
- Stable concepts (e.g., *"What is backpropagation?"*, *"How does attention calculate dot-product scaling?"*) **never** hit the web search tool; they are resolved via the curated static RAG store.
- Live web search triggers **only** when:
  1. The query classifier flags keywords indicating temporal recency or version changes (`latest`, `current version`, `release notes`, `newest`).
  2. The static RAG reranker fails to return any chunk with a relevance score $> 0.50$ for an evolving category topic.

## Rationale & Trade-offs
- **Positives:**
  - Protects user experience by keeping 80% of queries within the sub-second static RAG latency budget.
  - Lowers search API consumption by an estimated 75%.
- **Negatives:**
  - Queries that subtly touch upon recent framework deprecations might default to static RAG if not detected by the classifier.
  - *Mitigation:* Include an explicit toggle in the web UI allowing the user to force "Deep Web Research" manually.
