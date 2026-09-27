# Lab 01 step patches

These patches remove mechanical code editing without hiding the instrumentation. Each
file is a normal, readable Git patch against `application/main.py`.

Use them in number order from the corrected `lab-01-start-v2` checkpoint. The original
`lab-01-start` tag remains the immutable historical v1 checkpoint:

```bash
python scripts/lab_step.py list
python scripts/lab_step.py show 01
python scripts/lab_step.py apply 01
```

`show` prints every line that will change. `apply` checks that the patch fits the
current file, prints it again, and asks before changing anything. After applying a
step, inspect the ordinary working-tree diff:

```bash
git diff -- application/main.py
```

The steps are intentionally small:

| Step | What changes | What it teaches |
|---|---|---|
| `01-status-label` | Adds one route that can return 200 or 500 | One route can produce multiple status-labelled time series |
| `02-cardinality-problem` | Labels with `user_id` while middleware records raw paths | Unbounded values create unbounded time series |
| `03-normalize-cardinality` | Uses route templates and a bounded endpoint label | Metric labels describe stable dimensions |
| `04-gauge-negative-bug` | Adds an active-jobs gauge with an intentional decrement bug | Gauges move up and down; application semantics still matter |
| `05-guard-gauge` | Prevents active jobs from going below zero | Instrumentation should preserve domain invariants |
| `06-controlled-delay` | Adds a bounded, deterministic delay endpoint | Controlled latency populates histogram buckets predictably |

If a step does not apply, do not force it. Read the error, inspect `git diff`, and
check that all earlier numbered steps were applied. The patches never commit, reset,
or discard learner changes.
