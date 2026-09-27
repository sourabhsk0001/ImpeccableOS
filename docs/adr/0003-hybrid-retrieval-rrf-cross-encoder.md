# ADR 003: Hybrid Retrieval (Dense pgvector + Sparse PostgreSQL FTS) with Reciprocal Rank Fusion

## Status
**Accepted**

## Context
Pure dense vector retrieval frequently fails on AI engineering queries featuring exact acronyms, function names, parameter names, or version tags (e.g., `top_p`, `temperature`, `Claude 3.5 Sonnet`, `RunnablePassthrough`). Pure sparse search (BM25/FTS) fails on conceptual semantic queries (e.g., *"How do I keep agents from repeating actions?"*).

## Decision
Implement a **two-stage hybrid retrieval pipeline**:
1. Run dense cosine vector search using `pgvector` HNSW indexes ($top\ 20$).
2. Run sparse keyword search using PostgreSQL `tsvector` with `ts_rank_cd` ($top\ 20$).
3. Merge candidate sets using **Reciprocal Rank Fusion (RRF)** with constant $k=60$:
   $$RRF(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
4. Re-rank the top 20 fused candidates using a cross-encoder model (`cross-encoder/ms-marco-MiniLM-L-6-v2` or `FlashRank` for CPU efficiency) to select the final $3$ to $5$ context chunks.

## Rationale & Trade-offs
- **Positives:**
  - Outperforms dense-only retrieval by over $15\%$ in keyword-dense engineering domains.
  - Cross-encoder reranking eliminates false positives introduced by embedding cosine similarity compression.
- **Negatives:**
  - Adds ~150-250ms of compute latency for local cross-encoder scoring.
  - *Mitigation:* FlashRank or optimized ONNX models running on backend CPU keep rerank times below $100\text{ms}$.
