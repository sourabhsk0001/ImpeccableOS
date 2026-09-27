# Deterministic Agent State Loops & Model Context Protocol (MCP)

## Overview
Autonomous AI agents in enterprise systems must adhere to strict state transition invariants. Allowing an LLM to freely mutate state variables introduces prompt injection vulnerabilities, hallucinated parameters, and non-terminating execution loops.

## Deterministic Decoupling (ADR 002)
1. **Probabilistic Reasoning Phase:** The LLM receives structured schemas (Pydantic / JSON schema) to generate actions and parameter predictions.
2. **Deterministic Mutation Phase:** A strict finite-state engine validates transition preconditions, executes native Python logic, and updates state counters.

## Model Context Protocol (MCP) Integration
Model Context Protocol provides an open standard for LLM applications to access external tools and context servers:
- **Resources:** Static or dynamic data feeds read by the client.
- **Tools:** Callable routines executed with user-sanctioned permissions.
- **Prompts:** Reusable workflow templates provided by MCP hosts.
