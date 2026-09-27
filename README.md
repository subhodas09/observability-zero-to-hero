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

## Current progress

- [ ] Lab 00 — Published; fresh-clone validation pending
- [ ] Lab 01 — Coming next

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
