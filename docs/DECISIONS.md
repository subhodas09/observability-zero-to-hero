# Architecture & Curriculum Decisions

This file records meaningful project decisions.

Do not record trivial implementation details.

---

## ADR-001 — Local-first curriculum

### Decision

The core curriculum will run locally without requiring a cloud account.

### Why

Learners should be able to experiment freely, reproduce failures, and learn observability fundamentals without cloud cost or account dependencies.

### Current implementation

- macOS / Apple Silicon primary environment
- Python
- local FastAPI application

Cloud and AWS/EKS architecture will be introduced later as production mappings.

---

## ADR-002 — One evolving application

### Decision

Prefer one application that evolves throughout the curriculum instead of many disconnected demo applications.

### Why

This creates continuity and allows later incident labs to build on behavior learners already understand.

---

## ADR-003 — Progressive complexity

### Decision

Do not begin with Kubernetes or a full LGTM/OpenTelemetry stack.

### Why

Infrastructure complexity can hide observability fundamentals.

The progression should be approximately:

application
→ telemetry
→ Prometheus
→ Grafana
→ logging
→ tracing
→ OpenTelemetry
→ distributed services
→ Kubernetes
→ production patterns

---

## ADR-004 — FastAPI for the teaching application

### Decision

Use Python + FastAPI for the initial teaching application.

### Why

The application should contain minimal business complexity while still supporting realistic HTTP behavior, instrumentation, dependency calls, controlled failures, and telemetry.

---

## ADR-005 — Manual before automation

### Decision

Teach important operations manually before hiding them behind Makefiles, scripts, Helm, or other automation.

### Why

Automation should improve productivity after the learner understands the underlying operation.

---

## ADR-006 — Failure-driven learning

### Decision

Important observability concepts should be demonstrated through controlled experiments and failures whenever practical.

### Learning cycle

CONCEPT
→ PREDICT
→ BUILD
→ GENERATE TELEMETRY
→ OBSERVE
→ BREAK
→ INVESTIGATE
→ FIX
→ EXPLAIN
→ DOCUMENT

---

## ADR-007 — Repository is the long-term source of truth

### Decision

Project architecture, progress, decisions, curriculum, and teaching conventions should live in the repository.

### Why

Long-running ChatGPT and Codex sessions should not depend on historical chat context.

Repository governance files take precedence over stale chat context.
