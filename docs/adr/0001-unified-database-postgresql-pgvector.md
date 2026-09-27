# ADR 001: Unified Database Architecture (PostgreSQL + pgvector)

## Status
**Accepted**

## Context
The application requires both structured relational storage (user accounts, skill DAG nodes, dependency edges, assessment attempts, mastery histories) and high-performance vector similarity search for RAG embeddings. Dedicated vector databases (e.g., Pinecone, Milvus, Qdrant) are popular, but introducing an external vector store creates distributed transaction complexities, dual backup needs, and potential data synchronization mismatches.

## Decision
Use **PostgreSQL 16 with the `pgvector` extension** as the single primary database for all relational, structured state, and vector storage needs.

## Rationale & Trade-offs
- **Positives:**
  - ACID transactions across relational data and vector embeddings within a single engine.
  - Zero synchronization lag: deleting or updating a document removes its chunks and embeddings atomically.
  - Hybrid queries combining relational filters (e.g., `authority_level = 1 AND topic = 'rag'`) with vector distance (`<=>`) execute in a single SQL query planner pass.
  - Lower operational overhead and hosting cost for local development and production.
- **Negatives:**
  - PostgreSQL HNSW index build times and query throughput plateau around several million vectors compared to specialized C++ engines like Milvus or Qdrant.
  - *Mitigation:* The domain corpus for high-quality AI engineering documentation fits comfortably under 100,000 chunks, well within PostgreSQL's peak performance envelope.
