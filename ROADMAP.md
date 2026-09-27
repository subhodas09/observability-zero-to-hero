# Observability Zero → Hero — Roadmap

This roadmap defines the high-level learning progression for the project.

The exact lab numbering may evolve, but prerequisite order and progressive complexity should be preserved.

## Phase 0 — Environment & Observability Mental Model

- Monitoring vs observability
- Telemetry
- Metrics
- Logs
- Traces
- Correlation fundamentals
- First observable local application

Status: ✅ Complete

Completed lab:

- Lab 00 — Observability Fundamentals

## Phase 1 — Metrics Foundations

- Time series
- Counters
- Gauges
- Histograms
- Summaries
- Labels
- Dimensions
- Cardinality
- Metric design

Status: 🟡 In progress

Next lab:

- Lab 01 — Metrics Foundations

## Phase 2 — Prometheus

- Architecture
- Scraping
- Targets
- Exporters
- Service discovery
- TSDB fundamentals
- Retention
- Reliability

## Phase 3 — PromQL

- Selectors
- Instant vectors
- Range vectors
- Aggregation
- rate()
- increase()
- irate()
- Vector matching
- Histogram queries
- Recording rules

## Phase 4 — Grafana

- Data sources
- Dashboards
- Variables
- Panels
- Operational dashboard design
- Drill-down workflows

## Phase 5 — Logging

- Structured logging
- Log levels
- Correlation IDs
- Trace IDs
- Application and container logs
- Logging anti-patterns

## Phase 6 — Loki

- Architecture
- Streams
- Labels
- LogQL
- Parsing
- Kubernetes logging
- Cardinality

## Phase 7 — Distributed Tracing

- Traces
- Spans
- Parent/child relationships
- Attributes
- Events
- Propagation
- W3C Trace Context
- Multi-service requests

## Phase 8 — OpenTelemetry

- API
- SDK
- Manual instrumentation
- Automatic instrumentation
- Resources
- Semantic conventions
- OTLP

## Phase 9 — Tempo & Correlation

- Trace storage
- Trace search
- Grafana integration
- Metrics ↔ traces
- Logs ↔ traces
- Exemplars

## Phase 10 — Kubernetes Observability

- Pod/node/container telemetry
- kube-state-metrics
- Events
- Logs
- Resource limits
- CPU throttling
- OOMKilled
- CrashLoopBackOff
- Networking
- DNS
- Storage

## Phase 11 — Alerting

- Actionable alerts
- Symptom vs cause alerts
- Alertmanager
- Grouping
- Routing
- Inhibition
- Silencing
- Runbooks

## Phase 12 — SLI / SLO / SLA / Error Budgets

- SLIs
- SLOs
- SLAs
- Good events
- Valid events
- Error budgets
- Burn rate
- Multi-window alerts

## Phase 13 — Advanced Prometheus & Telemetry

- Recording rules
- Remote write
- Scaling
- Reliability
- Advanced histogram concepts
- Cardinality control

## Phase 14 — Profiling

- CPU profiles
- Memory profiles
- Flame graphs
- Pyroscope
- Tracing vs profiling

## Phase 15 — Telemetry Pipelines

- OpenTelemetry Collector
- Receivers
- Processors
- Exporters
- Queues
- Retries
- Backpressure
- Sampling

## Phase 16 — Cost / Scale / Reliability

- Metric volume
- Log volume
- Trace volume
- Retention
- Sampling
- Storage
- Cost optimization

## Phase 17 — Production Architecture

- High availability
- Security
- TLS
- Authentication
- Authorization
- Multi-cluster
- Multi-region
- Disaster recovery
- AWS/EKS mapping

## Phase 18 — Incident Response

- Incident investigation
- Hypothesis-driven debugging
- RCA
- Failure scenarios
- Observability improvements

## Phase 19 — Capstone

Build and operate a production-style distributed application.

The learner must:

- instrument it
- build dashboards
- define SLIs/SLOs
- create alerts
- correlate telemetry
- diagnose hidden incidents
- create an RCA
- propose production improvements

---

## Core progression rule

Do not introduce complexity before its prerequisites are understood.

The system should evolve gradually rather than becoming a large prebuilt observability stack.
