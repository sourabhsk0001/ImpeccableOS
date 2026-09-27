# Project Context & Domain Specification
## Project: ImpeccableOS - Adaptive AI Engineering Trainer & Execution Engine

---

## 1. Domain Background

The rapid evolution of modern Artificial Intelligence has fundamentally shifted software development from traditional deterministic code toward probabilistic, model-driven architectures. A discipline known as **AI Engineering** has emerged to bridge the gap between theoretical Machine Learning (ML) research and production-grade software development.

### The Problem
Traditional online learning solutions (e.g., Coursera, Udemy, generic documentation) and generic conversational LLMs suffer from severe structural shortcomings when training AI Engineers:
1. **Uncalibrated Model Confidence:** LLMs present incorrect architectural patterns with identical confidence to verified patterns, inducing bad habits in junior developers.
2. **Static Knowledge Decay:** The ecosystem (e.g., Model Context Protocol, LangGraph, vLLM, reasoning model patterns) evolves weekly. Static courses and LLM pretraining weights become obsolete within months.
3. **Passive Consumption vs. Evidence-Based Mastery:** Reading tutorials or watching videos creates an "illusion of competence." Without rigorous, multi-level evaluation across coding, debugging, and system design, genuine skill acquisition cannot be verified.
4. **Vague Chatbot Answers:** Typical LLM tutor interfaces provide ungrounded "vibes" rather than source-grounded engineering specifications backed by citations.

### The Solution: The Adaptive Trainer
The system functions as a **learning platform with an AI reasoning layer, rather than a generic chatbot**. It pairs a deterministic Directed Acyclic Graph (DAG) of AI engineering skills with hybrid retrieval, dynamic assessment, and automated web research to deliver personalized, verified learning paths.

---

## 2. Conceptual Architecture & System Topology

The platform enforces clean separation between three distinct tiers:

```
+-----------------------------------------------------------------------+
|                           APPLICATION LAYER                           |
|  - Next.js 14 App Router (React, Tailwind CSS, TypeScript)            |
|  - SSE Event Streaming & Interactive DAG Graph Visualizer (Cytoscape) |
|  - FastAPI Backend Application (Async endpoints, Pydantic validation) |
+-----------------------------------▲-----------------------------------+
                                    │ HTTP / SSE / JSON-RPC
+-----------------------------------▼-----------------------------------+
|                          INTELLIGENCE LAYER                           |
|  - Query Router & Intent Classifier                                   |
|  - Hybrid RAG Controller (pgvector + PostgreSQL Full-Text Search)     |
|  - FlashRank / Cross-Encoder Reranking Engine                         |
|  - Live Web Research Agent (Tavily Search + Freshness Gate)           |
|  - Deterministic Mastery & Adaptive Roadmapping Engine (DAG Traversal)|
|  - Assessment Engine (Pydantic-enforced evaluation & diagnostic logic)|
+-----------------------------------▲-----------------------------------+
                                    │ SQL / Embeddings / Traces
+-----------------------------------▼-----------------------------------+
|                            KNOWLEDGE LAYER                            |
|  - PostgreSQL 16 (Relational schemas, user state, graph dependencies) |
|  - pgvector extension (Cosine distance embeddings indexing)           |
|  - Structured Corpus (Official specs, papers, maintainer blogs)       |
|  - Structured Run Trace Log (Observability, Latency, Token Accounting)|
+-----------------------------------------------------------------------+
```

---

## 3. Skill Graph Taxonomy (Initial V1 Domain)

The skill graph models prerequisite relationships across five core disciplines:

```
                              AI Engineering
                                    │
    ┌────────────────┬──────────────┴───────────────┬────────────────┐
    │                │                              │                │
Software Eng    AI Fundamentals             LLM Engineering      Production AI
    │                │                              │                │
 ├── Python      ├── Vector Math                ├── Tokenization  ├── Eval Benchmarks
 ├── REST APIs   ├── Linear Algebra             ├── Embeddings    ├── Latency/Cost
 ├── Async IO    ├── Feedforward NNs            ├── Structured    ├── Observability
 └── Databases   └── Attention & Transformers        Outputs      └── Guardrails
                                                ├── Tool Calling
                                                    │
                                                    ▼
                                           ┌─────────────────┐
                                           │  RAG Systems    │
                                           │  ├── Chunking   │
                                           │  ├── Hybrid FTS │
                                           │  ├── Reranking  │
                                           │  └── Context    │
                                           └────────┬────────┘
                                                    │
                                                    ▼
                                           ┌─────────────────┐
                                           │ Agent Systems   │
                                           │ ├── State Loops │
                                           │ ├── Memory      │
                                           │ ├── Multi-Agent │
                                           │ └── MCP Tooling │
                                           └─────────────────┘
```

Each node stores:
- `skill_id`: Unique identifier (e.g., `rag.hybrid_search`).
- `name`: Human-readable label (e.g., "Hybrid Lexical/Semantic Search").
- `prerequisites`: Array of required parent IDs (`['rag.chunking', 'rag.vector_search']`).
- `mastery_threshold`: Minimal score required to clear the node ($0.70$).
- `rubric`: Criteria for Level 1 (Recall) through Level 5 (System Design).

---

## 4. Grounding and Confidence Calculation Framework

To prevent model hallucination from misinforming learners, answers are evaluated using a multi-factor grounding pipeline:

```
User Query
    │
    ▼
Hybrid Retrieval (pgvector + FTS)
    │
    ▼
Top 20 Chunks
    │
    ▼
Cross-Encoder Reranker
    │
    ├─► If max(Reranker_Score) < 0.50 & Topic == Evolving ──► Trigger Web Research
    │
    ▼
Top 3 to 5 Chunks (Filtered by relevance)
    │
    ▼
LLM Generation with Citation Constraints
    │
    ▼
Grounding Calibration Verifier
    ├── Retrieval Relevance (Cross-Encoder score mean)
    ├── Source Authority (Domain metadata tier)
    └── Semantic Entailment (Claims vs. Chunks mapping)
    │
    ▼
Composite Confidence Score + Citation Badges attached to Answer
```

---

## 5. User Journey Walkthrough

1. **Onboarding & Goal Selection:** The user authenticates and selects a career objective (e.g., *"Agentic AI Systems Engineer"*).
2. **Diagnostic Evaluation:** The system generates a diagnostic test across the root-to-goal path on the DAG.
3. **Roadmap Initialization:** Unsatisfied prerequisites are ordered via topological sort to build a dynamic, non-linear study plan.
4. **Interactive Learning & Grounded Chat:** The learner works through modules. When asking questions, the tutor answers using retrieved documentation, complete with verifiable inline citations and a confidence audit badge.
5. **Practical Assessment:** The learner completes coding challenges or short-answer architectural questions. The deterministic evaluation engine updates mastery scores using an Exponential Moving Average.
6. **Adaptive Re-planning:** If mastery drops or improves, the roadmap engine recalculates the downstream path and explicitly notifies the learner: *"Roadmap updated: 'Agent Memory' unlocked based on scoring 85% in 'State Loops'."*
