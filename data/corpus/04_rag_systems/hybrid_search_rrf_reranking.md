# Hybrid Lexical and Dense Semantic Search with Reciprocal Rank Fusion (RRF)

## Executive Summary
In production AI engineering, relying solely on dense vector retrieval introduces critical blind spots when encountering exact code identifiers, system metrics, acronyms, or model tags. Conversely, pure sparse search (e.g., BM25 or PostgreSQL Full-Text Search `tsvector`) fails to resolve conceptual semantics.

## Architecture
The hybrid pipeline operates in two distinct phases:

### Phase 1: Candidate Generation
1. **Dense Cosine Retrieval:** Executes vector distance calculation using PostgreSQL 16 with `pgvector` indexed via Hierarchical Navigable Small World (HNSW):
   $$\text{Distance} = 1 - \frac{u \cdot v}{\|u\|_2 \|v\|_2}$$
2. **Sparse Lexical Search:** Queries PostgreSQL `tsvector` with `ts_rank_cd` covering technical terminology.

### Phase 2: Reciprocal Rank Fusion & Reranking
Combining dense cosine scores and sparse BM25 scores via linear weighted addition is brittle because their score distributions are uncalibrated and shift dynamically. Reciprocal Rank Fusion (RRF) bypasses scale calibration by fusing ordinal ranks:

$$RRF(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

Where:
- $M$: The set of retrieval models (dense vector search and sparse keyword search).
- $r_m(d)$: The 1-indexed rank of document $d$ within ranking model $m$.
- $k$: Smoothing constant set to $60$.

Top fused candidates ($top\ 20$) are then reranked through a cross-encoder model to produce the final $3$ to $5$ context passages.
