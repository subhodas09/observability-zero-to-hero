# Lab 00 — Observability Fundamentals

🟢 **Difficulty:** Beginner

## What you'll learn

By the end of this lab, you will understand:

- monitoring vs observability
- what telemetry means
- the purpose of metrics
- the purpose of logs
- the purpose of traces
- how metrics, logs, and traces complement each other
- what a Prometheus counter represents
- the basic meaning of histogram `_count`, `_sum`, and `_bucket`
- how a `trace_id` can correlate telemetry
- how to investigate a simple application problem using telemetry

Most importantly, you will **run a real application and inspect real telemetry**.

---

## Why this matters

Observability is not primarily about installing tools such as Grafana, Prometheus, Loki, or Tempo.

Those are tools used to collect, store, query, and visualize telemetry.

The more important skill is learning how to answer questions such as:

- Is the application healthy?
- Are requests failing?
- Has latency increased?
- Which requests are affected?
- Where is a request spending its time?
- What happened when a failure occurred?

In this lab we intentionally avoid a large observability stack.

We will first understand the signals themselves.

---

## Mental model

A running system produces evidence about its behavior.

That evidence is called **telemetry**.

```text
                    APPLICATION
                         │
                         │ emits
                         ▼
                      TELEMETRY
                         │
              ┌──────────┼──────────┐
              │          │          │
              ▼          ▼          ▼
           METRICS      LOGS      TRACES
```

A useful starting mental model is:

### Metrics

Answer questions about system behavior **at scale**.

Examples:

- How many requests are arriving?
- How many are failing?
- Is latency increasing?
- Is CPU usage increasing?

### Logs

Record discrete events and associated context.

Examples:

- Which endpoint was called?
- What error occurred?
- Which user-visible operation failed?
- What was happening around a request?

### Traces

Describe the execution path of an individual operation.

Examples:

- Which service was slow?
- Was the database responsible for latency?
- How long did a downstream dependency take?
- Where did a particular request fail?

A useful troubleshooting flow is often:

```text
METRICS
What is happening at scale?
        │
        ▼
TRACES
Where inside the request is it happening?
        │
        ▼
LOGS
What detailed event/context explains it?
```

This is not a strict rule.

Real incident investigations are hypothesis-driven, and any signal may provide the first useful clue.

---

# Monitoring vs observability

Monitoring usually asks questions that we already know are important.

For example:

```text
Alert if error rate > 5%
```

or:

```text
Alert if CPU usage > 90%
```

Observability helps us investigate questions whose exact cause may not be known in advance.

For example:

```text
Users say checkout became slow.

Why?
```

Possible causes could include:

```text
application
database
cache
network
DNS
downstream service
CPU
memory
retries
timeouts
```

Telemetry gives us evidence for forming and testing hypotheses.

---

# Architecture

The architecture for this lab is intentionally small.

```text
You / curl
     │
     ▼
 FastAPI application
     │
     ├── Metrics
     │
     ├── Logs
     │
     └── Traces
```

We are **not** using:

- Kubernetes
- Prometheus server
- Grafana
- Loki
- Tempo
- OpenTelemetry Collector

Those will be introduced progressively later.

---

# Files used

From the repository root:

```text
application/
├── __init__.py
└── main.py

requirements.txt
```

The application contains several intentionally simple endpoints:

| Endpoint | Purpose |
|---|---|
| `/health` | Healthy fast request |
| `/slow` | Intentionally slow request |
| `/error` | Intentionally returns HTTP 500 |
| `/metrics/` | Exposes Prometheus-format metrics |

---

# Prerequisites

You need:

- Python 3.10 or newer
- terminal access
- `curl`
- Git

Check Python:

```bash
python3 --version
```

Check curl:

```bash
curl --version
```

---

# Step 1 — Create the Python environment

From the repository root:

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

# Step 2 — Start the application

Run:

```bash
uvicorn application.main:app --reload --port 8000
```

Expected output should contain something similar to:

```text
Uvicorn running on http://127.0.0.1:8000
```

Keep this terminal open.

Open another terminal for the following commands.

---

# Step 3 — Establish a healthy baseline

Run:

```bash
curl http://localhost:8000/health
```

Expected:

```json
{"status":"healthy"}
```

✅ If you see this response, the application is running correctly.

---

# Step 4 — Predict before generating traffic

We are going to send three types of requests:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/slow
curl http://localhost:8000/error
```

Before running them, predict:

1. Which endpoint will have the highest latency?
2. Which endpoint will return HTTP 500?
3. Should separate requests have the same trace ID or different trace IDs?

Make your prediction before continuing.

---

# Step 5 — Generate telemetry

Healthy request:

```bash
curl http://localhost:8000/health
```

Slow request:

```bash
curl http://localhost:8000/slow
```

The response should take approximately two seconds.

Error request:

```bash
curl -i http://localhost:8000/error
```

Expected:

```text
HTTP/1.1 500 Internal Server Error
```

We have now generated three different behaviors:

```text
healthy
slow
failed
```

Now we can observe them.

---

# Step 6 — Inspect logs

Look at the terminal running Uvicorn.

You should see JSON output similar to:

```json
{
  "event": "http_request_completed",
  "method": "GET",
  "path": "/slow",
  "status": 200,
  "duration_seconds": 2.001,
  "trace_id": "...",
  "span_id": "..."
}
```

The exact values will be different.

This log lets us answer questions such as:

```text
Which endpoint?
What HTTP method?
What status code?
How long did the request take?
Which trace belongs to the request?
```

Mental model:

```text
LOG = discrete event + context
```

---

# Step 7 — Inspect traces

The application also exports OpenTelemetry spans directly to the console for learning purposes.

You should see something conceptually similar to:

```text
"name": "GET /slow"

"trace_id": "0x..."

"span_id": "0x..."

"attributes": {
    "http.request.method": "GET",
    "url.path": "/slow",
    "http.response.status_code": 200,
    "request.duration_seconds": ...
}
```

For now, use this mental model:

```text
TRACE
└── journey of an operation

SPAN
└── one unit of work inside that journey
```

Our application currently has a very simple trace:

```text
Trace
└── GET /slow ≈ 2 seconds
```

Later in the course, the same idea will evolve toward:

```text
GET /checkout
│
├── API Gateway
├── Order Service
│   ├── Redis
│   └── PostgreSQL
└── Product Service
```

---

# Step 8 — Inspect metrics

Run:

```bash
curl -s http://localhost:8000/metrics/ | grep lab00_
```

> Notice the trailing `/` in `/metrics/`.

You should see metrics including:

```text
lab00_http_requests_total
```

and:

```text
lab00_http_request_duration_seconds
```

---

## Request counter

You may see something similar to:

```text
lab00_http_requests_total{
  endpoint="/health",
  method="GET",
  status="200"
} 3
```

This means:

```text
3 GET requests to /health returned HTTP 200
```

The metric name is:

```text
lab00_http_requests_total
```

The labels are:

```text
endpoint="/health"
method="GET"
status="200"
```

The current value is:

```text
3
```

Think of it as:

```text
metric name
+
label combination
=
a distinct time series
```

We will study time series and cardinality deeply in later labs.

---

# Step 9 — Understand the counter

Run:

```bash
curl -s http://localhost:8000/health > /dev/null
```

Inspect the metric again:

```bash
curl -s http://localhost:8000/metrics/ \
  | grep 'lab00_http_requests_total'
```

The `/health` counter should increase.

Conceptually:

```text
0 → 1 → 2 → 3 → 4 → ...
```

Counters represent values that accumulate over time.

A process restart can reset them.

We will explore that behavior later.

---

# Step 10 — Basic histogram understanding

Find:

```text
lab00_http_request_duration_seconds_count
```

and:

```text
lab00_http_request_duration_seconds_sum
```

Suppose `/slow` shows:

```text
_count = 2
_sum   ≈ 4 seconds
```

This means:

```text
2 requests were observed

total observed request duration ≈ 4 seconds
```

Average latency can therefore be approximated with:

```text
sum / count
```

So:

```text
4 / 2
≈ 2 seconds
```

This matches the intentionally slow behavior of the endpoint.

---

# Step 11 — Understand histogram buckets

You may see:

```text
_bucket{endpoint="/slow",le="1.0"} 0
_bucket{endpoint="/slow",le="2.5"} 2
_bucket{endpoint="/slow",le="5.0"} 2
```

`le` means:

```text
less than or equal to
```

Therefore:

```text
le="1.0" → 0
```

means:

> Zero observed `/slow` requests completed within one second.

And:

```text
le="2.5" → 2
```

means:

> Two observed `/slow` requests completed within 2.5 seconds.

Prometheus histogram buckets are cumulative.

If a request completes in approximately two seconds, then it is also true that it completed within:

```text
≤ 2.5 seconds
≤ 5 seconds
≤ 10 seconds
≤ infinity
```

Do not worry about percentiles or `histogram_quantile()` yet.

Those will be covered later.

---

# Experiment — Predict histogram changes

First inspect the current `/slow` values.

Then generate five more slow requests:

```bash
for i in {1..5}; do
  curl -s http://localhost:8000/slow > /dev/null
done
```

Before inspecting the metrics again, predict:

```text
_count = ?

_sum ≈ ?

_bucket{le="1.0"} = ?
```

If there were previously two `/slow` requests:

```text
_count should become 7

_sum should become approximately 14 seconds

le="1.0" should remain 0
```

Now verify:

```bash
curl -s http://localhost:8000/metrics/ \
  | grep 'lab00_http_request_duration_seconds_.*endpoint="/slow"'
```

Compare your prediction with reality.

---

# Step 12 — Compare successful, slow, and failed behavior

An important lesson is that latency and errors are different dimensions.

For example:

```text
/health
fast + successful

/slow
slow + successful

/error
fast + failed
```

A system can therefore be:

```text
fast + successful
fast + failing
slow + successful
slow + failing
```

Looking at only one signal can hide important behavior.

---

# Step 13 — Correlate logs and traces

Generate one slow request:

```bash
curl -s http://localhost:8000/slow
```

In the application terminal, find the JSON log and the corresponding span.

The log should contain:

```text
trace_id
span_id
```

The OpenTelemetry span should contain the same identifiers, although the console representation may include a hexadecimal `0x` prefix.

Conceptually:

```text
LOG

trace_id=abc123
      │
      │ same request
      ▼
TRACE

trace_id=abc123
```

This is our first example of **telemetry correlation**.

Later this becomes:

```text
metric anomaly
      ↓
trace
      ↓
slow span
      ↓
related logs
```

---

# Operational mental model

Suppose the service handles 100,000 requests and users report slow responses.

Would you:

```text
A. Read 100,000 logs

B. Inspect aggregated latency metrics

C. Open random traces
```

A sensible starting point is:

```text
B — aggregated metrics
```

Metrics help determine:

```text
whether latency increased
when it increased
which endpoint is affected
how severe the problem is
```

Then traces can help localize latency inside individual operations.

Then logs can provide detailed contextual information.

---

# What each signal tells us

## Metrics

Useful for:

```text
What is happening at scale?
```

Examples:

- request rate
- errors
- latency
- resource utilization

---

## Traces

Useful for:

```text
Where inside this operation did something happen?
```

Examples:

- slow database call
- slow downstream service
- failing dependency
- retry chain

---

## Logs

Useful for:

```text
What detailed event/context occurred?
```

Examples:

- error message
- exception details
- retry message
- business/application event

---

# Troubleshooting lesson — `/metrics` returns 307

You may accidentally run:

```bash
curl http://localhost:8000/metrics
```

and receive:

```text
HTTP/1.1 307 Temporary Redirect
```

The metrics exporter is mounted as a sub-application.

The correct URL is:

```text
http://localhost:8000/metrics/
```

Notice the trailing slash.

You can prove the redirect:

```bash
curl -i http://localhost:8000/metrics
```

Look for a `Location` header pointing to:

```text
/metrics/
```

Then:

```bash
curl -i http://localhost:8000/metrics/
```

should return:

```text
HTTP/1.1 200 OK
```

This is also a small example of hypothesis-driven troubleshooting:

```text
SYMPTOM

metrics command returns nothing

        ↓

OBSERVATION

HTTP 307

        ↓

HYPOTHESIS

request is being redirected

        ↓

VERIFY

curl -i

        ↓

CAUSE

correct endpoint is /metrics/
```

---

# Common problems

## `uvicorn: command not found`

Make sure the virtual environment is activated:

```bash
source .venv/bin/activate
```

Then install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## Port 8000 already in use

Check which process is using the port:

```bash
lsof -i :8000
```

Either stop that process or temporarily use another port:

```bash
uvicorn application.main:app --reload --port 8001
```

Remember to update the `curl` commands accordingly.

---

## `/metrics` gives HTTP 307

Use:

```bash
curl -i http://localhost:8000/metrics/
```

The response should begin with `HTTP/1.1 200 OK` and include Prometheus-format metrics.

---

# Cleanup

In the terminal running Uvicorn, press `Ctrl+C` to stop the application. Wait for shutdown to finish and the shell prompt to return.

Then deactivate the Python virtual environment in that terminal:

```bash
deactivate
```

If you activated the virtual environment in any other terminal, run `deactivate` there too.

---

# Next steps

Before moving on, make sure you can:

- reproduce healthy, slow, and failed requests
- explain how the request counter and histogram change when you generate traffic
- find a request log and console span with matching trace and span identifiers
- explain why `/metrics/` includes a trailing slash
- stop the application and deactivate the virtual environment

Lab 00 is currently in final repository preparation. The second commit, GitHub publication, and validation from a fresh clone are still pending; see [Project Progress](../../docs/PROGRESS.md) for the remaining work.

After Lab 00 publication validation is complete, continue to **Metrics Foundations** in the [roadmap](../../ROADMAP.md). The next lab has not been published yet; return to the [project README](../../README.md) for its entry point when available.
