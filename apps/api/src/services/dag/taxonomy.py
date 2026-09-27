from typing import Dict, List, Any

INITIAL_TAXONOMY: List[Dict[str, Any]] = [
    # 1. Software Engineering
    {
        "id": "swe.python_async",
        "domain": "software_engineering",
        "name": "Async I/O & Concurrency in Python",
        "description": "Mastery of asyncio event loops, coroutines, non-blocking network calls, and backpressure management.",
        "depth_level": 1,
        "mastery_threshold": 0.70,
        "prerequisites": []
    },
    {
        "id": "swe.rest_apis",
        "domain": "software_engineering",
        "name": "Production REST & SSE Streaming APIs",
        "description": "Designing high-throughput asynchronous endpoints, FastAPI dependencies, SSE streaming, and client connection management.",
        "depth_level": 1,
        "mastery_threshold": 0.70,
        "prerequisites": ["swe.python_async"]
    },
    {
        "id": "swe.databases",
        "domain": "software_engineering",
        "name": "Relational Data Modeling & Indexing",
        "description": "PostgreSQL schema design, ACID transactions, B-Tree and GIN indexing, and connection pooling.",
        "depth_level": 1,
        "mastery_threshold": 0.70,
        "prerequisites": []
    },

    # 2. AI Fundamentals
    {
        "id": "ai.vector_math",
        "domain": "ai_fundamentals",
        "name": "High-Dimensional Vector Math",
        "description": "Dot products, cosine similarity, Euclidean distance, L2 normalization, and curse of dimensionality.",
        "depth_level": 1,
        "mastery_threshold": 0.70,
        "prerequisites": []
    },
    {
        "id": "ai.attention_transformers",
        "domain": "ai_fundamentals",
        "name": "Attention Mechanisms & Transformer Architecture",
        "description": "Scaled dot-product attention, multi-head attention, positional encoding, and KV-cache mechanics.",
        "depth_level": 2,
        "mastery_threshold": 0.75,
        "prerequisites": ["ai.vector_math"]
    },

    # 3. LLM Engineering
    {
        "id": "llm.tokenization",
        "domain": "llm_engineering",
        "name": "Tokenization Mechanics & Context Limits",
        "description": "Byte-pair encoding (BPE), vocabulary distributions, token cost accounting, and context window truncation strategies.",
        "depth_level": 2,
        "mastery_threshold": 0.70,
        "prerequisites": ["ai.attention_transformers"]
    },
    {
        "id": "llm.embeddings",
        "domain": "llm_engineering",
        "name": "Dense Embedding Generation & Indexing",
        "description": "Embedding models, pooling layers, HNSW vs. IVFFlat indexing in vector databases.",
        "depth_level": 2,
        "mastery_threshold": 0.70,
        "prerequisites": ["ai.vector_math", "swe.databases"]
    },
    {
        "id": "llm.structured_outputs",
        "domain": "llm_engineering",
        "name": "Deterministic Structured Outputs & Constrained Decoding",
        "description": "Grammar-based sampling, JSON schema enforcement via Pydantic, and resilient parsing pipelines.",
        "depth_level": 2,
        "mastery_threshold": 0.75,
        "prerequisites": ["swe.python_async", "llm.tokenization"]
    },
    {
        "id": "llm.tool_calling",
        "domain": "llm_engineering",
        "name": "Native Function Calling & Execution Runtimes",
        "description": "Declarative tool definitions, error handling, parameter coercion, and function routing loop.",
        "depth_level": 3,
        "mastery_threshold": 0.75,
        "prerequisites": ["llm.structured_outputs", "swe.rest_apis"]
    },

    # 4. RAG Systems
    {
        "id": "rag.chunking",
        "domain": "rag_systems",
        "name": "Semantic & Recursive Document Chunking",
        "description": "Token-aware sliding windows, AST code chunking, markdown header splitting, and chunk overlap tuning.",
        "depth_level": 3,
        "mastery_threshold": 0.70,
        "prerequisites": ["llm.embeddings"]
    },
    {
        "id": "rag.hybrid_fts",
        "domain": "rag_systems",
        "name": "Hybrid Lexical/Dense Retrieval & Reciprocal Rank Fusion",
        "description": "Combining PostgreSQL tsvector FTS with pgvector dense cosine search via Reciprocal Rank Fusion (k=60).",
        "depth_level": 3,
        "mastery_threshold": 0.80,
        "prerequisites": ["rag.chunking", "swe.databases"]
    },
    {
        "id": "rag.reranking",
        "domain": "rag_systems",
        "name": "Cross-Encoder Reranking & Context Compression",
        "description": "Two-stage retrieval pipelines, FlashRank ONNX models, and score normalization.",
        "depth_level": 4,
        "mastery_threshold": 0.80,
        "prerequisites": ["rag.hybrid_fts"]
    },

    # 5. Agent Systems
    {
        "id": "agent.state_loops",
        "domain": "agent_systems",
        "name": "Deterministic Agent State Machines & Loops",
        "description": "State transition graphs, ReAct decision loops, cycle limits, and deterministic state mutation.",
        "depth_level": 4,
        "mastery_threshold": 0.80,
        "prerequisites": ["llm.tool_calling"]
    },
    {
        "id": "agent.memory",
        "domain": "agent_systems",
        "name": "Agent Memory Architectures (Episodic & Semantic)",
        "description": "Short-term buffer memory, long-term semantic retrieval, scratchpads, and context compression.",
        "depth_level": 4,
        "mastery_threshold": 0.75,
        "prerequisites": ["agent.state_loops", "rag.hybrid_fts"]
    },
    {
        "id": "agent.mcp_tooling",
        "domain": "agent_systems",
        "name": "Model Context Protocol (MCP) Integration",
        "description": "Standardized MCP JSON-RPC protocol, tool servers, resource providers, and client security sandboxing.",
        "depth_level": 4,
        "mastery_threshold": 0.80,
        "prerequisites": ["agent.state_loops"]
    },

    # 6. Production AI
    {
        "id": "prod.eval_benchmarks",
        "domain": "production_ai",
        "name": "LLM Evaluation, Benchmarking & Synthetic Datasets",
        "description": "RAG triad evaluations (faithfulness, answer relevance, context precision), LLM-as-a-judge calibration.",
        "depth_level": 5,
        "mastery_threshold": 0.85,
        "prerequisites": ["rag.reranking", "agent.state_loops"]
    },
    {
        "id": "prod.observability",
        "domain": "production_ai",
        "name": "Observability, Structured Tracing & Cost Accounting",
        "description": "OpenTelemetry spans, prompt latency distributions, token cost accounting, and audit logging.",
        "depth_level": 5,
        "mastery_threshold": 0.80,
        "prerequisites": ["prod.eval_benchmarks"]
    }
]


def build_canonical_graph() -> "DAGEngine":
    from src.services.dag.engine import DAGEngine
    engine = DAGEngine()
    for skill in INITIAL_TAXONOMY:
        engine.add_skill(
            skill_id=skill["id"],
            name=skill["name"],
            domain=skill["domain"],
            threshold=skill["mastery_threshold"]
        )
    for skill in INITIAL_TAXONOMY:
        for prereq in skill["prerequisites"]:
            engine.add_prerequisite(prereq, skill["id"])
    return engine
