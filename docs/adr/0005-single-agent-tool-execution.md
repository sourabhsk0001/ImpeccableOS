# ADR 005: Single-Agent Tool Execution Before Multi-Agent Topology

## Status
**Accepted**

## Context
Beginning with an unconstrained multi-agent framework (e.g., AutoGen, CrewAI, multi-actor supervisor setups) introduces non-deterministic execution loops, high token consumption, massive debugging latency, and frequent state corruption.

## Decision
Implement the runtime as a **single, deterministic agent runtime with explicit tool definitions** executed via native function calling. Multi-agent delegation (Supervisor $\to$ Tutor / Researcher / Assessor) will be introduced only after individual tool runtimes maintain $\ge 90\%$ task success rates under evaluation suites.

## Rationale & Trade-offs
- **Positives:**
  - Predictable execution graphs that can be traced with OpenTelemetry or structured JSON logs.
  - Avoids runaway agent execution loops and uncontrolled token costs.
  - Faster initial time-to-market for the core MVP loop.
- **Negatives:**
  - Complex tasks requiring concurrent research and cross-examination are sequenced rather than parallelized.
