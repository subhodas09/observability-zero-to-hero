# Project Progress

This file is the current operational state of the Observability Zero → Hero project.

Future ChatGPT and Codex sessions should read this file before substantial work.

## Current phase

Phase 1 — Metrics Foundations

## Current lab

Lab 00 — Observability Fundamentals

Status: ✅ Complete

## Completed

- Created local Git repository
- Created Python virtual environment
- Built first FastAPI application
- Added `/health`
- Added `/slow`
- Added `/error`
- Added Prometheus-compatible `/metrics/`
- Added structured JSON request logs
- Added basic OpenTelemetry console tracing
- Generated healthy traffic
- Generated slow traffic
- Generated HTTP 500 failures
- Inspected raw metrics
- Learned basic counter behavior
- Learned histogram `_count`, `_sum`, and cumulative buckets
- Correlated logs and traces using `trace_id`
- Diagnosed `/metrics` → `/metrics/` HTTP 307 redirect
- Created public Lab 00 README
- Created root README
- Curated direct Python dependencies
- Verified application from a clean temporary virtual environment
- Committed governance files and documentation corrections in `d40c287`: `AGENTS.md`, `ROADMAP.md`, `docs/PROGRESS.md`, `docs/DECISIONS.md`, and both READMEs
- Created the public [GitHub repository](https://github.com/subhodas09/observability-zero-to-hero)
- Configured `origin`, pushed both initial commits on `main`, and verified public visibility and the remote commit
- Set the repository description and all 14 requested topics
- Verified the public repository from a completely fresh clone
- Verified dependency installation from `requirements.txt`
- Verified `/health`
- Verified `/slow`
- Verified `/error`
- Verified `/metrics/`
- Verified repository navigation and required project files

## Current architecture

```text
User / curl
     |
     v
FastAPI application
     |
     +-- Prometheus-format metrics
     |
     +-- Structured JSON logs
     |
     +-- OpenTelemetry console spans
```

Prometheus server, Grafana, Loki, Tempo, Kubernetes, and OpenTelemetry Collector have not been introduced yet. The application exposes Prometheus-format metrics and uses the OpenTelemetry SDK to export spans to the console.

## Current application endpoints

| Endpoint | Current behavior |
|---|---|
| `/health` | Returns HTTP 200 with a healthy status |
| `/slow` | Waits approximately two seconds, then returns HTTP 200 |
| `/error` | Returns an intentional HTTP 500 failure |
| `/metrics/` | Exposes Prometheus-format metrics; the trailing slash avoids a redirect |

## Current important files

- `README.md` — project introduction, prerequisites, and lab entry point
- `labs/00-observability-fundamentals/README.md` — Lab 00 instructions, verification, troubleshooting, and cleanup
- `application/main.py` — FastAPI endpoints, metrics, structured logs, and console tracing
- `application/__init__.py` — application package marker
- `requirements.txt` — pinned direct Python dependencies
- `.gitignore` — excludes the virtual environment and generated local files
- `AGENTS.md` — project governance and contributor instructions
- `ROADMAP.md` — curriculum progression
- `docs/DECISIONS.md` — architecture and curriculum decisions
- `docs/PROGRESS.md` — current project state and remaining work

## Unresolved work

No unresolved Lab 00 blockers.

## Next

Lab 01 — Metrics Foundations

Focus:

- time series
- counters
- gauges
- labels
- dimensions
- first principles of metric design

Do not introduce the Prometheus server yet unless the lab explicitly reaches that prerequisite.
