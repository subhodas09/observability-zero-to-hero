# Lab 01 — Metrics Foundations

🟢 **Difficulty:** Beginner

## What you will learn

By the end of this lab, you will be able to:

- explain why a metric name plus one label combination is one time series
- distinguish a Counter, Gauge, and Histogram
- predict how status labels split requests into separate series
- recognize unbounded labels and raw dynamic paths as cardinality risks
- normalize dynamic paths to stable route templates
- observe a Counter reset after a process restart
- explain Gauge up/down behavior and protect a Gauge from invalid application state
- read histogram `_bucket`, `_count`, `_sum`, and `_created` samples
- subtract cumulative buckets to find observations inside one bucket
- calculate simple and grouped weighted averages
- estimate p50, p80, p90, p95, and p99 with classic-histogram linear interpolation
- explain why tail latency can be unhealthy while average latency looks acceptable
- choose bounded labels for application metrics

This lab still reads metrics directly from the application. A Prometheus server and
PromQL arrive in later labs.

## Prerequisites

Complete [Lab 00](../00-observability-fundamentals/README.md) first. You need:

- Python 3.10 or newer
- Git
- `curl`
- a terminal

## Start from the Lab 01 checkpoint

Course checkpoints use immutable annotated tags. `main` represents the latest
reviewed course state, while each lab has two checkpoints:

- `lab-N-start` is the environment prepared for learning Lab N: the previous lab's
  application baseline plus the new lab's instructions, patches, helpers, and tests.
- `lab-N-complete` is the reviewed reference implementation after finishing Lab N.

Learners normally branch from the start checkpoint. For Lab 01, new learners should
use the corrected v2 start checkpoint:

```bash
git clone https://github.com/subhodas09/observability-zero-to-hero.git
cd observability-zero-to-hero
git switch -c learner/lab-01 lab-01-start-v2
```

The new branch keeps your experiments separate. It starts with the completed Lab 00
application and also includes this README, the step patches, `scripts/lab_step.py`,
the percentile helper, and its tests.

Keep both checkpoint types for every future lab. A version suffix is used only when
an already-published checkpoint needs an additive correction:

```text
lab-01-start-v2
lab-01-complete
lab-02-start
lab-02-complete
...
```

`lab-00-complete` remains useful as the finished Lab 00 reference and should point to
`ca0f15a77c78e17c8eee7e111462c05a19a0f3ae`. It is not the normal Lab 01 starting
point because that commit does not contain the Lab 01 course assets.

`lab-01-start-v2` contains the corrected learner guide while `application/main.py`
remains identical to the Lab 00 application baseline. The original `lab-01-start`
tag remains published as the historical v1 checkpoint and is never moved.
`lab-01-complete` remains the reviewed final application where all six steps have
been applied.

Tags are course releases. Do not move or reuse an existing checkpoint tag. This lab
documents the strategy; tags are created only when the corresponding course state is
reviewed and published.

## Set up the application

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Start the application in terminal 1:

```bash
uvicorn application.main:app --reload --port 8000
```

Keep it running. Use terminal 2 for requests and metric inspection. Activate the
environment there too:

```bash
source .venv/bin/activate
```

Verify the baseline:

```bash
curl -s http://localhost:8000/health
curl -s http://localhost:8000/metrics/ | grep 'lab00_'
```

The trailing slash in `/metrics/` is required.

## How to restart the app during this lab

Use terminal 1, where Uvicorn is running. Press `Ctrl+C` and wait until the shell
prompt returns. From the repository root, activate the virtual environment if the
prompt does not already show `(.venv)`, then start the app again:

```bash
source .venv/bin/activate
uvicorn application.main:app --reload --port 8000
```

Keep Uvicorn running in terminal 1. Run learner commands, requests, and metric
inspection in terminal 2.

The `--reload` option usually reloads saved Python edits automatically. A reload or a
restart creates a new process and therefore clears process-local metric state. When an
exercise needs an exact starting value, this guide explicitly asks for a deliberate
`Ctrl+C` stop and start so Counters, Gauges, and Histograms begin cleanly.

## How code changes work in this lab

Each teaching change is a small Git patch in `steps/`. The patch is the lesson
artifact: it is readable, reviewable, and uses normal Git diff syntax. The helper only
shows or applies that patch. It does not generate hidden code, commit, reset, or discard
your work.

List the steps:

```bash
python scripts/lab_step.py list
```

For every step, use this learning loop:

```text
READ WHY → PREDICT → SHOW → APPLY → GENERATE TRAFFIC → OBSERVE → EXPLAIN
```

Example:

```bash
python scripts/lab_step.py show 01
python scripts/lab_step.py apply 01
git diff -- application/main.py
```

`apply` prints the patch again and asks for confirmation. Manual editing is always an
option, but it is not required for these mechanical changes. Read the patch before
applying it: the instrumentation is part of what you are learning.

Apply the numbered steps in order. If a step fails its safety check, inspect:

```bash
git diff -- application/main.py
```

Do not use a force option. Compare your file with the displayed patch and resolve the
overlap deliberately.

---

# Part 1 — Counter labels and time series

The existing request Counter is:

```python
REQUEST_COUNT = Counter(
    "lab00_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)
```

A Counter represents a cumulative total. It normally moves in one direction:

```text
0 → 1 → 2 → 3 → ...
```

The process can restart, which creates a reset. The observation system must account
for resets when calculating rates later.

The metric name alone is not a time series. Each distinct label set is a separate time
series:

```text
lab00_http_requests_total{method="GET",endpoint="/health",status="200"}
lab00_http_requests_total{method="GET",endpoint="/error",status="500"}
```

## Step 01 — Same route, different status

Read the purpose of the first patch in [steps/README.md](steps/README.md). Then predict:

1. If `/variable-status` returns both 200 and 500, how many Counter series will that
   route produce?
2. Which label changes between those series?

Show and apply the change:

```bash
python scripts/lab_step.py show 01
python scripts/lab_step.py apply 01
```

Generate both outcomes:

```bash
curl -i 'http://localhost:8000/variable-status'
curl -i 'http://localhost:8000/variable-status?fail=true'
```

Observe:

```bash
curl -s http://localhost:8000/metrics/ \
  | grep 'lab00_http_requests_total.*endpoint="/variable-status"'
```

You should find separate series with `status="200"` and `status="500"`.

Explain in your own words: why did one route create two time series even though the
metric name stayed the same?

## Counter reset experiment

First generate three healthy requests:

```bash
for i in 1 2 3; do curl -s http://localhost:8000/health > /dev/null; done
```

Read the current series:

```bash
curl -s http://localhost:8000/metrics/ \
  | grep 'lab00_http_requests_total.*endpoint="/health".*status="200"'
```

Predict what the value will be immediately after the application process restarts.
Follow [How to restart the app during this lab](#how-to-restart-the-app-during-this-lab),
make one `/health` request, and inspect the same series. This deliberate restart clears
the Counter's in-memory value so the reset is observable.

The Counter starts again from process-local state. A reset does not mean requests were
undone. Later, Prometheus functions such as `rate()` and `increase()` will account for
these resets.

---

# Part 2 — Cardinality and bounded labels

Cardinality is the number of distinct time series. Every unique label-value combination
creates another series.

> **Core rule:** request volume changes metric values; label diversity changes
> cardinality.

Bounded values have a known, small set:

```text
method = GET, POST, PUT, DELETE
status = 200, 404, 500
route  = /health, /error, /cardinality/{user_id}
```

Unbounded values keep growing:

```text
user_id = alice, bob, user-10492, ...
request_id = one new value per request
raw path = /users/1, /users/2, /users/3, ...
```

## Step 02 — Create the bad design deliberately

This step makes two related mistakes for observation:

- `lab01_user_requests_total` uses `user_id` as a label
- the existing middleware records `request.url.path`, so each raw dynamic path also
  becomes an `endpoint` label value

Predict how many new time series three different user IDs will create. Then:

```bash
python scripts/lab_step.py show 02
python scripts/lab_step.py apply 02
```

Generate requests:

```bash
curl -s http://localhost:8000/cardinality/alice
curl -s http://localhost:8000/cardinality/bob
curl -s http://localhost:8000/cardinality/charlie
```

Inspect both metrics:

```bash
curl -s http://localhost:8000/metrics/ \
  | grep 'lab01_user_requests_total'
```

```bash
curl -s http://localhost:8000/metrics/ \
  | grep 'lab00_http_requests_total.*cardinality'
```

You should see user IDs in one label and raw paths such as `/cardinality/alice` in the
other. Imagine one million users: the application would create at least one series per
user or raw path. That makes storage, queries, and memory more expensive.

Now prove the core rule with a controlled 100-user experiment. First follow
[How to restart the app during this lab](#how-to-restart-the-app-during-this-lab) to
remove the three earlier user series. Then run:

```bash
for i in $(seq 1 100); do
  curl -s "http://localhost:8000/cardinality/user-$i" > /dev/null
done

curl -s http://localhost:8000/metrics/ \
  | grep '^lab01_user_requests_total{' \
  | wc -l
```

Expected series count: `100`. Sending more requests for the same 100 users increases
the existing Counter values but keeps the series count at 100. A request from
`user-101` adds a label value and therefore a new series. Explain how this demonstrates:

```text
request volume changes metric values
label diversity changes cardinality
```

## Step 03 — Normalize the labels

The route already has a stable template:

```text
/cardinality/{user_id}
```

The fix uses that template as the bounded endpoint label and removes `user_id` from the
metric label set. The response and request log may still contain the real path when it
is useful; the metric dimension stays bounded.

Predict what label value Alice, Bob, and Charlie will share after a restart. Then:

```bash
python scripts/lab_step.py show 03
python scripts/lab_step.py apply 03
```

Follow [How to restart the app during this lab](#how-to-restart-the-app-during-this-lab)
so the old metric definitions and high-cardinality in-memory series are removed.
Generate the same requests:

```bash
for user in alice bob charlie; do
  curl -s "http://localhost:8000/cardinality/$user" > /dev/null
done
```

Observe:

```bash
curl -s http://localhost:8000/metrics/ \
  | grep 'lab01_user_requests_total'
```

```bash
curl -s http://localhost:8000/metrics/ \
  | grep 'lab00_http_requests_total.*cardinality'
```

All three requests should accumulate into stable series with:

```text
endpoint="/cardinality/{user_id}"
```

Explain why route templates are appropriate for metrics while individual user IDs are
better kept in logs or traces when policy permits.

## Bounded-label design rules

Before adding a metric label, ask:

1. Can I list the possible values in advance?
2. Can this value grow with users, requests, orders, URLs, or time?
3. Will an operator aggregate or filter by this dimension?
4. Would a route template or category answer the same question?
5. Is this high-cardinality context better suited to a log or trace?

Good first choices include method, normalized route, outcome, dependency name, and a
small status class. Avoid user IDs, request IDs, trace IDs, timestamps, raw URLs, email
addresses, and arbitrary error messages.

---

# Part 3 — Gauges and state invariants

A Gauge represents a value that can move up or down:

```text
active jobs: 0 → 1 → 2 → 1 → 0
```

Other examples include queue depth, temperature, memory in use, and concurrent
requests. A Gauge is not automatically valid just because it can decrease. The
application must preserve the meaning of the measured state.

## Step 04 — Observe an intentional negative-Gauge bug

This step adds start and finish operations, but finish always decrements. Predict the
Gauge value after calling finish once while no job is active.

```bash
python scripts/lab_step.py show 04
python scripts/lab_step.py apply 04
```

Follow [How to restart the app during this lab](#how-to-restart-the-app-during-this-lab)
so the Gauge starts from zero, then run:

```bash
curl -s http://localhost:8000/gauge/jobs/finish
curl -s http://localhost:8000/metrics/ | grep '^lab01_active_jobs '
```

The Gauge becomes `-1`. The metric library allowed it because negative Gauges are
valid for some domains, such as temperature. It is invalid for this domain because the
number of active jobs cannot be negative.

Continue the experiment:

```bash
curl -s http://localhost:8000/gauge/jobs/start
curl -s http://localhost:8000/gauge/jobs/start
curl -s http://localhost:8000/gauge/jobs/finish
curl -s http://localhost:8000/metrics/ | grep '^lab01_active_jobs '
```

Explain why metric type alone cannot enforce application meaning.

## Step 05 — Add the application guard

The fix decrements only when `active_jobs > 0`.

```bash
python scripts/lab_step.py show 05
python scripts/lab_step.py apply 05
```

Follow [How to restart the app during this lab](#how-to-restart-the-app-during-this-lab)
so the Gauge and guarded application state both start from zero. Then call finish twice:

```bash
curl -s http://localhost:8000/gauge/jobs/finish
curl -s http://localhost:8000/gauge/jobs/finish
curl -s http://localhost:8000/metrics/ | grep '^lab01_active_jobs '
```

Expected:

```text
lab01_active_jobs 0.0
```

Then verify normal up/down semantics:

```bash
curl -s http://localhost:8000/gauge/jobs/start
curl -s http://localhost:8000/gauge/jobs/start
curl -s http://localhost:8000/gauge/jobs/finish
curl -s http://localhost:8000/metrics/ | grep '^lab01_active_jobs '
```

Expected value: `1.0`.

---

# Part 4 — Histograms, averages, and percentiles

The application already observes request duration with a classic Prometheus Histogram:

```python
REQUEST_DURATION = Histogram(
    "lab00_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["endpoint"],
)
```

It exposes four related sample families:

```text
..._bucket{le="..."}  cumulative observations at or below a boundary
..._count             total observations
..._sum               total duration of all observations
..._created           Unix timestamp when this labelled histogram series was created
```

The Python client exposes `_created` as seconds since the Unix epoch. It is useful when
you need to understand when a process-local series appeared, but it is usually not
central to latency analysis. Bucket counts, `_count`, and `_sum` describe the latency
distribution itself.

## Step 06 — Add controlled latency

The `/delay` endpoint accepts a bounded delay from 0 through 5000 milliseconds. It
makes bucket experiments repeatable.

The `ms` query parameter controls application behavior, but it is intentionally not a
metric label. Arbitrary delay values would keep creating label values and increase
cardinality. The bounded route label stays `endpoint="/delay"` for every allowed delay.

Predict which default histogram buckets a 300 ms request will increment. Then:

```bash
python scripts/lab_step.py show 06
python scripts/lab_step.py apply 06
```

Uvicorn may reload the applied code automatically. Verify the endpoint from terminal 2:

```bash
curl -s 'http://localhost:8000/delay?ms=300'
```

Expected:

```json
{"requested_delay_ms":300}
```

The parameter guard is also observable:

```bash
curl -i 'http://localhost:8000/delay?ms=6000'
```

Expected status: `422 Unprocessable Entity`.

Those two verification requests were observed by the `/delay` histogram. Before the
controlled distribution, follow
[How to restart the app during this lab](#how-to-restart-the-app-during-this-lab).
This deliberate reset removes the verification traffic so the next ten requests are
the histogram's only `/delay` observations. Do not call `/delay` again before running
the loop.

Generate a controlled distribution:

```bash
for ms in 50 80 120 180 220 300 400 700 1200 2000; do
  curl -s "http://localhost:8000/delay?ms=$ms" > /dev/null
done
```

Inspect only `/delay` buckets:

```bash
curl -s http://localhost:8000/metrics/ \
  | grep 'lab00_http_request_duration_seconds_.*endpoint="/delay"'
```

The output should include:

```text
lab00_http_request_duration_seconds_count{endpoint="/delay"} 10.0
```

If the count is not 10, restart once more and repeat only the ten-request loop.

Exact timing varies slightly because real request handling adds overhead.

## Cumulative bucket subtraction

Suppose two cumulative buckets are:

```text
le="0.25"  6
le="0.50"  9
```

The number of observations in `(0.25, 0.50]` is:

```text
9 - 6 = 3
```

Do not add cumulative buckets together. A request in the 0.25-second bucket is already
included in every larger bucket.

## Average latency

For one endpoint:

```text
average = _sum / _count
```

If `_sum` is 5.25 seconds and `_count` is 10:

```text
average = 5.25 / 10 = 0.525 seconds
```

An average compresses the whole distribution into one number. Nine fast requests and
one very slow request may have the same average as ten medium requests, even though
their user impact differs.

### Required grouped weighted-average exercise

A simple average gives every individual observation equal weight. When observations
are summarized in groups, multiply each group value by its request count before
dividing by the total request count.

Suppose 5 requests take 100 ms each and 10 requests take 300 ms each. Before revealing
the answer, calculate:

1. the total latency contributed by each group
2. the combined total latency
3. the total request count
4. the grouped weighted-average latency

Do not use `(100 + 300) / 2`: that simple average treats the two groups as equal even
though the second group contains twice as many requests.

<details>
<summary>Check your calculation</summary>

```text
first group  = 5 × 100 ms  = 500 ms
second group = 10 × 300 ms = 3000 ms
total latency = 3500 ms
total requests = 5 + 10 = 15
weighted average = 3500 / 15 ≈ 233.33 ms
```

</details>

## Percentiles and tail latency

p50 is the estimated value at or below which 50% of observations fall. p80, p90, p95,
and p99 mean that 80%, 90%, 95%, and 99% of observations respectively fall at or
below the estimated value. A percentile does not mean that percentage of requests took
exactly that value. p95 and p99 describe the slow tail more directly than an average.

Classic histograms do not retain every individual duration. They retain cumulative
bucket counts. When a target falls inside a bucket, estimate its position with linear
interpolation:

```text
target count = percentile × total observations

observations in bucket = current cumulative - previous cumulative

fraction through bucket =
    (target count - previous cumulative) / observations in bucket

estimate = previous upper bound + fraction × bucket width
```

This assumes observations are spread evenly inside the selected bucket. The result is
an estimate, and bucket design controls its possible precision.

## Required manual calculation — do this before using the helper

Use these cumulative buckets:

| Upper bound | Cumulative observations |
|---:|---:|
| 0.10 s | 12 |
| 0.25 s | 28 |
| 0.50 s | 43 |
| 1.00 s | 50 |

Calculate p80 by hand. Write down:

1. total observations
2. target count
3. previous and current bucket
4. observations inside the selected bucket
5. position and fraction through that bucket
6. bucket width
7. estimated p80

Do not run the next command until you have an answer.

Your calculation should be:

```text
total = 50
target = 0.80 × 50 = 40
selected bucket = (0.25, 0.50]
observations in bucket = 43 - 28 = 15
position in bucket = 40 - 28 = 12
fraction = 12 / 15 = 0.8
width = 0.50 - 0.25 = 0.25 seconds
p80 ≈ 0.25 + 0.8 × 0.25 = 0.45 seconds
```

Now exercise p90 with the same buckets before using the helper. The target count is
`0.90 × 50 = 45`, so locate the first cumulative bucket at or above 45 and interpolate
inside it.

<details>
<summary>Check your p90 calculation</summary>

```text
selected bucket = (0.50, 1.00]
observations in bucket = 50 - 43 = 7
position in bucket = 45 - 43 = 2
fraction = 2 / 7
width = 1.00 - 0.50 = 0.50 seconds
p90 ≈ 0.50 + (2 / 7) × 0.50 ≈ 0.642857 seconds
```

This means an estimated 90% of observations are at or below about 0.643 seconds.

</details>

Now verify rather than replace your reasoning:

```bash
python tools/histogram_percentile.py \
  --buckets '0.10:12,0.25:28,0.50:43,1.00:50' \
  --percentile 80
```

The helper prints every calculation step. It accepts numeric or `p`-prefixed values:

```bash
python tools/histogram_percentile.py \
  --buckets '0.10:12,0.25:28,0.50:43,1.00:50' \
  --percentiles p50,p80,p90,p95,p99
```

## Verify percentiles from live `/delay` metrics

After generating `/delay` traffic, pipe the raw Prometheus exposition into the helper:

```bash
curl -s http://localhost:8000/metrics/ \
  | python tools/histogram_percentile.py \
      --metric lab00_http_request_duration_seconds \
      --label endpoint=/delay \
      --percentiles p50,p90,p95,p99
```

The label filter matters because the histogram has separate series for `/health`,
`/slow`, `/delay`, and other routes. If multiple series match, the helper asks you to
choose one rather than silently combining them.

Compare p50 with p90, p95, and p99. A large gap indicates a long latency tail. Then inspect
the raw buckets again and explain which slow requests created that gap.

In later Prometheus and PromQL labs, you will use `histogram_quantile()` across stored
time series. This helper exists now to expose the bucket subtraction and interpolation
that query function performs conceptually. It is a learning and verification tool,
not a replacement for PromQL.

---

# Choosing a metric type

| Question | Metric type | Example |
|---|---|---|
| How many events have occurred? | Counter | total HTTP requests |
| What is the current level? | Gauge | active jobs |
| What is the distribution of measured values? | Histogram | request duration |

Choose a Counter for totals that accumulate and may reset when the process restarts.
Choose a Gauge for current state that legitimately rises and falls. Choose a Histogram
when distribution, thresholds, averages, and percentiles matter.

Knowledge check:

1. Total failed login attempts: Counter, Gauge, or Histogram?
2. Current queue depth: Counter, Gauge, or Histogram?
3. Request duration: Counter, Gauge, or Histogram?
4. Why is `user_id` unsafe as a metric label?
5. Why can p99 reveal a problem that an average hides?

Answers: Counter, Gauge, Histogram; user IDs are unbounded; p99 describes the slowest
tail while an average blends fast and slow observations.

## Troubleshooting

### A patch says it cannot apply

Run:

```bash
git diff -- application/main.py
python scripts/lab_step.py list
```

Confirm that you started from `lab-01-start-v2` and applied earlier steps in number
order. Do not discard your file automatically; read the overlap.

### Metrics still show old label series

The client library keeps series in process memory. Follow
[How to restart the app during this lab](#how-to-restart-the-app-during-this-lab) after
changing label definitions, then generate new traffic.

### The app is not reachable from terminal 2

Confirm that terminal 1 still shows Uvicorn running on `http://127.0.0.1:8000`. If it
does not, follow [How to restart the app during this lab](#how-to-restart-the-app-during-this-lab).
Keep terminal 1 running while you retry the `curl` command in terminal 2.

### `/metrics` returns 307

Use the trailing slash:

```bash
curl -i http://localhost:8000/metrics/
```

### The helper reports multiple series

Add a stable label filter, for example:

```bash
--label endpoint=/delay
```

### A percentile lands in `+Inf`

An infinite-width bucket cannot be linearly interpolated. The helper returns the
previous finite upper bound and explains the limitation. In a real system, add a useful
finite bucket boundary for the range you need to measure.

## Cleanup

Stop Uvicorn with `Ctrl+C`, wait for the prompt, then run:

```bash
deactivate
```

Keep the `learner/lab-01` branch if you want to revisit your experiments.

## Before leaving this lab

Make sure you can:

- show why labels create separate time series
- reproduce and fix the raw-path and user-ID cardinality problem
- reproduce a Counter reset
- reproduce and fix the negative active-jobs Gauge
- subtract cumulative histogram buckets
- calculate at least one percentile manually
- calculate a grouped weighted average before checking the answer
- define and use p50, p80, p90, p95, and p99 as `at or below` estimates
- use the helper to verify p50, p90, p95, and p99
- explain Counter vs Gauge vs Histogram selection
- defend every label as bounded and operationally useful

## Planned application structure for Lab 02

`application/main.py` now contains tracing setup, metric definitions, middleware, and
experiment routes. It is still small enough to keep unchanged in this package, which
avoids a distracting refactor during Lab 01.

Before adding more Lab 02 experiments, split by teaching responsibility:

```text
application/
├── main.py                         application creation and route assembly
├── instrumentation/
│   ├── metrics.py                  metric definitions
│   └── middleware.py               HTTP observation middleware
└── experiments/
    └── metrics.py                  controlled metric-learning endpoints
```

Keep route behavior obvious and imports shallow. The refactor should be its own
transparent step so learners can see where instrumentation lives before new concepts
are added.
