# Observability Zero → Hero

Learn observability by **building, breaking, observing, and troubleshooting real systems**.

This is a hands-on, open-source observability course that progresses from first principles to production-level observability and SRE practices.

> No cloud account required.
> Everything begins locally.

## Learn by doing

The learning cycle is:

CONCEPT → PREDICT → BUILD → GENERATE TELEMETRY → OBSERVE → BREAK → INVESTIGATE → FIX → EXPLAIN → DOCUMENT

This repository is not intended to become a collection of YAML files that deploy an observability stack.

The goal is to understand **how observability actually works through experiments**.

## What we'll build

The system will evolve gradually:

Simple application → Metrics → Prometheus → PromQL → Grafana → Structured Logging → Loki → Distributed Tracing → OpenTelemetry → Tempo → Kubernetes Observability → Alerting → SLOs → Profiling → Production Architecture → Incident Response

Complexity is introduced only when it teaches something useful.

## Start here

### 🟢 Lab 00 — Observability Fundamentals

Run a real application and inspect:

- metrics
- logs
- traces
- healthy requests
- slow requests
- failed requests

You will also learn the first mental model for using telemetry during troubleshooting.

➡️ [Start Lab 00](labs/00-observability-fundamentals/README.md)

### 🟢 Lab 01 — Metrics Foundations

Learn how Counters, Gauges, Histograms, labels, cardinality, averages, and percentile
interpolation work through controlled application experiments.

➡️ [Start Lab 01](labs/01-metrics-foundations/README.md)

## Current progress

- [x] Lab 00 — Observability Fundamentals
- [x] Lab 01 — Metrics Foundations (published and validated from a fresh clone)
- [ ] Lab 02 — Prometheus Fundamentals (next)

Lab 01's corrected learner workflow covers all 34 audited learning and usability
criteria. The v2 start checkpoint, six-step workflow, percentile helper, and final
application were validated from a fresh clone.

## Technology

The course will progressively use:

- Python
- FastAPI
- Docker
- Kubernetes / Minikube
- Prometheus
- Grafana
- Loki
- Tempo
- OpenTelemetry
- OpenTelemetry Collector
- Pyroscope
- k6

Not all tools are required at the beginning.

## Prerequisites

For Lab 00 you only need:

- Git
- Python 3.10 or newer
- curl
- a terminal

Later labs introduce additional dependencies only when needed.

## Course checkpoints

Each lab normally uses two immutable annotated tags with different purposes:

- `lab-N-start` is the prepared environment for learning Lab N. It contains the
  previous lab's application baseline plus the instructions, patches, helpers, and
  tests needed to complete Lab N.
- `lab-N-complete` is the reviewed reference implementation after Lab N is finished.

Learners normally create their working branch from `lab-N-start`. Use
`lab-N-complete` to inspect the finished state, compare work, recover, or jump ahead.
The two tags must identify distinct course states when the lab changes the application.

Published tags are never moved. If published course material needs a correction, a
new versioned tag is added while the original remains available.

For Lab 01, new learners should use the corrected start checkpoint:

```bash
git clone https://github.com/subhodas09/observability-zero-to-hero.git
cd observability-zero-to-hero
git switch -c learner/lab-01 lab-01-start-v2
```

`lab-01-start` is the historical published v1 checkpoint. `lab-01-start-v2` keeps the
same Lab 00 application baseline and adds the corrected learner documentation.
`lab-01-complete` remains the final Lab 01 application reference.

## Supported environment

Primary:

- macOS
- Apple Silicon

Linux support will also be provided where practical.

## Repository philosophy

1. Learn the concept before automating it.
2. Establish healthy behavior before introducing failures.
3. Use telemetry to test hypotheses.
4. Prefer one evolving application over disconnected demos.
5. Introduce complexity only when it teaches something useful.
6. Every public lab must work without access to our ChatGPT conversation.

## Project status

🚧 **Under active development**

The goal is to build a complete practical path from:

**Observability Zero → Production-Level Observability & SRE Skills**

## License

A license will be added before the first public release.
