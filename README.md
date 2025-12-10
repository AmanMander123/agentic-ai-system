# Production-Grade AI Agent Stack 

Building a transparent, production-ready virtual assistant stack in public: from web UI to retrieval, tool-use, observability, and CI/CD. Follow along for real-world patterns, not demos.

![System Diagram](agentic-ai-system-design.png)

## What this is
- Public journey of shipping an end-to-end agent platform.
- Focused on reliability, observability, secure config, and repeatable deployments.
- Regular updates with design notes, benchmarks, and failure postmortems.

## Architecture (from the diagram)
- Web App UI → FastAPI API (REST/WebSocket) with streaming responses.
- Infra & CI/CD guardrails: deploys, secrets, rollbacks.
- Queue (Pub/Sub/SQS) for async/parallel work; workers for jobs/metrics.
- Agent Orchestrator: prompt routing, tool chaining, JSON payloads, streamed replies.
- LLM calls + Tooling Layer (internal APIs, 3rd-party tools).
- Retrieval Layer (hybrid RAG) over Knowledge Stores: vector DB (embeddings) + docs DB (text+metadata).
- Ingestion Pipeline (chunks, embeds, index) feeding the stores.
- Observability everywhere: logs, traces, metrics.

## Roadmap
- [ ] Stand up API skeleton (typing, auth, streaming).
- [ ] Observability baseline (structured logs, tracing, metrics).
- [ ] Retrieval + ingestion pipeline (chunking, embeddings, hybrid search).
- [ ] Agent orchestration patterns (tool routing, retries, guards).
- [ ] Frontend for fast UX + live streaming.
- [ ] CI/CD with lint/tests, env templates, deploy scripts.
- [ ] Benchmarks, evals, and red-team scenarios.

## Principles
- Production-first: error budgets, retries, circuit breakers, timeouts.
- Secure-by-default: no secrets in repo; `.env.example` + secret manager usage.
- Reproducible: pinned deps, make/just tasks, CI parity with local.
- Observable: every hop emits traces/metrics/logs.

## How to follow
- Regular repo updates; threads on X for milestones and lessons.
- Issues will track work items; PRs welcome once the baseline lands.

## Status
- Kickoff ✅: diagram + plan in place.
- Backend scaffold ✅: FastAPI app with `/health` and `/agent/query`. The agent endpoint uses `openai-agents` and pulls the OpenAI API key from GCP Secret Manager (no secrets in repo), keyed by `GCP_PROJECT_ID` + secret name.

## Next steps (options under evaluation)
- **Output guardrails**: JSON schema/Pydantic validation; retries/repair; OpenAI JSON mode; Guardrails.ai/Outlines; moderation/safety filters (OpenAI/Vertex/custom regex); risk-based escalation to human/clarify.
- **Prompts + grounding**: versioned prompt templates; RAG with hybrid search (pgvector/Pinecone/Qdrant/Weaviate); retrieval scoring gates; schema checks before output; fallbacks when context is weak.
- **Structured autonomy**: LangGraph/state machines for planning; tool allowlists with input/output validation and rate limits; step/depth caps; scoped memory (conversation window + summaries + retrieval memory); dead-end detection with graceful handoff.
- **Observability**: OpenTelemetry tracing across app/LLM/tools; structured logs with trace IDs; metrics for latency/token/rate limits/guardrail outcomes; LangSmith/Arize Phoenix for LLM traces/evals; store prompt/response versions for replay and offline evals.
