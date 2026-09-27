# Project Progress

This file is the current operational state of the Observability Zero → Hero project.

Future ChatGPT and Codex sessions should read this file before substantial work.

## Current phase

Phase 2 — Prometheus

## Current lab

Lab 02 — Prometheus Fundamentals

Status: 🟡 Next — Lab 01 is complete and publicly reproducible

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
- Prepared `scripts/lab_step.py` plus six readable patches that support the learner loop:
  read why → predict → show → apply → generate traffic → observe → explain
- Prepared the standard-library `tools/histogram_percentile.py` verifier for direct bucket
  exercises and raw Prometheus exposition text
- Prepared deterministic percentile tests, including p75 ≈ 0.4167 seconds and p80 =
  0.45 seconds
- Prepared the public Lab 01 learner guide with exact commands, troubleshooting, cleanup,
  metric-selection guidance, bounded-label rules, and the Lab 02 refactor plan
- Completed the six Lab 01 application steps: status-labelled Counter series, the
  cardinality failure and normalized-route fix, the negative-Gauge failure and guard,
  and bounded controlled latency
- Validated Lab 01 syntax, percentile tests and examples, step ordering and safety,
  application endpoints, metric series, histogram accumulation, and raw-metrics
  percentile parsing
- Published and verified the immutable `lab-00-complete`, `lab-01-start`, and
  `lab-01-complete` annotated checkpoint tags
- Validated the complete Lab 01 learner step workflow from a fresh public clone
- Confirmed the learner-built `application/main.py` is byte-for-byte identical to
  the `lab-01-complete` checkpoint
- Validated the percentile helper and final application from clean public checkouts
- Confirmed Lab 01 is publicly reproducible

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
| `/delay?ms=...` | Waits for a validated delay from 0 through 5000 ms; invalid values return HTTP 422 |
| `/error` | Returns an intentional HTTP 500 failure |
| `/variable-status` | Returns HTTP 200 by default or an intentional HTTP 500 with `fail=true` |
| `/cardinality/{user_id}` | Demonstrates a dynamic route while metrics use the bounded route template |
| `/gauge/jobs/start` | Increments the active-jobs Gauge |
| `/gauge/jobs/finish` | Decrements the Gauge without allowing it to become negative |
| `/metrics/` | Exposes Prometheus-format metrics; the trailing slash avoids a redirect |

## Current important files

- `README.md` — project introduction, prerequisites, and lab entry point
- `labs/00-observability-fundamentals/README.md` — Lab 00 instructions, verification, troubleshooting, and cleanup
- `labs/01-metrics-foundations/README.md` — Lab 01 concepts, experiments, exact commands, and checks
- `labs/01-metrics-foundations/steps/` — readable, sequential code patches and their purpose
- `application/main.py` — FastAPI endpoints, metrics, structured logs, and console tracing
- `scripts/lab_step.py` — shows and safely applies one learner step patch
- `tools/histogram_percentile.py` — explains classic-histogram percentile interpolation
- `tests/test_histogram_percentile.py` — deterministic standard-library validation
- `application/__init__.py` — application package marker
- `requirements.txt` — pinned direct Python dependencies
- `.gitignore` — excludes the virtual environment and generated local files
- `AGENTS.md` — project governance and contributor instructions
- `ROADMAP.md` — curriculum progression
- `docs/DECISIONS.md` — architecture and curriculum decisions
- `docs/PROGRESS.md` — current project state and remaining work

## Unresolved work

- None for Lab 01.

## Next

Begin Lab 02 — Prometheus Fundamentals. Split the growing application into
`application/instrumentation/` and
`application/experiments/` before adding more experiments. Then begin Prometheus server
fundamentals. Do not introduce Grafana, Kubernetes, or unrelated stack components yet.
