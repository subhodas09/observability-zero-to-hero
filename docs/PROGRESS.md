# Project Progress

This file is the current operational state of the Observability Zero → Hero project.

Future ChatGPT and Codex sessions should read this file before substantial work.

## Current phase

Phase 0 — Environment & Observability Mental Model

## Current lab

Lab 00 — Observability Fundamentals

Status: Published; fresh-clone validation pending

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

- Validate setup and Lab 00 from a fresh clone of the published repository.
- Add a license before the first public release, as noted in the root README.

GitHub publication is complete. Lab 00 remains incomplete until validation from a fresh clone succeeds.

## Next

1. From a fresh clone of the published repository, verify installation, application startup, endpoints, telemetry, and cleanup.
2. Record the validation result here and mark Lab 00 complete only after publication validation succeeds.
3. Continue to Metrics Foundations in `ROADMAP.md` once Lab 00 is complete.
