# Project Progress

This file is the current operational state of the Observability Zero → Hero project.

Future ChatGPT and Codex sessions should read this file before substantial work.

## Current phase

Phase 0 — Environment & Observability Mental Model

## Current lab

Lab 00 — Observability Fundamentals

Status: Final repository preparation

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
- Created and staged governance files: `AGENTS.md`, `ROADMAP.md`, `docs/PROGRESS.md`, and `docs/DECISIONS.md`

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

- Review and stage the documentation corrections; the previously staged governance files do not yet include these corrections.
- Create the second commit for project governance, the roadmap, and documentation corrections.
- Create the GitHub repository and publish the local commits.
- Validate setup and Lab 00 from a fresh clone of the published repository.
- Add a license before the first public release, as noted in the root README.

The second commit, GitHub publication, and fresh-clone validation remain pending. Lab 00 remains in final repository preparation until publication validation is complete.

## Next

1. Review the repaired documentation and run `git diff --check` and `git status`.
2. Stage the reviewed corrections and create the second commit when ready.
3. Publish to GitHub, then verify installation, application startup, endpoints, telemetry, and cleanup from a fresh clone.
4. Record the validation result here and mark Lab 00 complete only after publication validation succeeds.
5. Continue to Metrics Foundations in `ROADMAP.md` once Lab 00 is complete.
