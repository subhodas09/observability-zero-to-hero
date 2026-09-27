# AGENTS.md — Observability Zero → Hero

## Read this first

This repository is both:

1. a hands-on observability learning project
2. a public beginner-to-advanced open-source course

The objective is not merely to make infrastructure work.

The learner must understand why it works.

---

## Mandatory startup rule

Before substantial implementation, refactoring, architectural changes, or new labs, read:

1. `AGENTS.md`
2. `ROADMAP.md`
3. `docs/DECISIONS.md`
4. `docs/PROGRESS.md`
5. the current lab README
6. relevant architecture documentation

Do not rely only on chat history.

Repository governance files are the long-term source of truth.

---

## Project philosophy

Use this learning cycle whenever practical:

CONCEPT
→ PREDICT
→ BUILD
→ GENERATE TELEMETRY
→ OBSERVE
→ BREAK
→ INVESTIGATE
→ FIX
→ EXPLAIN
→ DOCUMENT

Do not turn the repository into a collection of unexplained YAML or configuration files.

---

## Progressive complexity

Do not introduce technology merely to make the project look advanced.

Avoid prematurely introducing:

- Kubernetes
- service meshes
- Kafka
- multiple unnecessary microservices
- cloud infrastructure
- large observability stacks

Complexity must teach something valuable.

---

## Manual before automation

Do not hide educational steps behind automation before they have been taught manually.

Example:

First understand how Prometheus starts and reads its configuration.

Only later introduce convenience commands such as:

`make observability-up`

---

## Course-authoring workflow

**Automate the mechanics, never automate the learning.**

Apply this principle to every future lab:

- ChatGPT remains the instructor and coach: introduce concepts, guide reasoning, ask for predictions, help interpret results, and check understanding.
- Work/Codex handles locating files, mechanical or repetitive code and configuration edits, large YAML changes, validation, and repository maintenance.
- Learners remain hands-on for predictions, observability commands, telemetry inspection, PromQL, LogQL, Kubernetes troubleshooting, incident investigation, verification, and knowledge checks.
- Require manual editing only when the edit is small and performing it teaches the concept.
- Helpers, patches, and scripts may apply mechanical changes, but they must show learners what changes, explain why it changes, and preserve the PREDICT → APPLY → OBSERVE → EXPLAIN loop.
- Do not hide concept-defining instrumentation behind opaque automation. Surface and explain the instrumentation that teaches the concept before it is applied.

---

## Public documentation requirement

Every public lab must be usable by someone who has never seen the development conversation.

A lab is not complete unless a learner can:

- understand its purpose
- understand prerequisites
- follow setup instructions
- run commands
- verify success
- understand important commands/configuration
- troubleshoot common failures
- perform cleanup
- know what comes next

---

## Application philosophy

The application exists to teach observability.

Keep business logic simple.

It should progressively support:

- normal requests
- slow requests
- failures
- database calls
- cache calls
- downstream requests
- retries
- timeouts
- controlled fault injection
- instrumentation

---

## Current architecture

Read `docs/PROGRESS.md` for the authoritative current architecture.

Do not assume future components already exist.

---

## Documentation conventions

Early labs:

- exact commands
- explanations
- expected output
- verification
- troubleshooting

Intermediate labs:

- progressively less hand-holding

Advanced/incident labs:

- symptoms
- constraints
- telemetry
- investigation goals

Do not immediately reveal incident root causes.

---

## Architecture decisions

Before changing established technologies, architecture, curriculum ordering, or repository conventions:

1. check `docs/DECISIONS.md`
2. identify conflicts
3. explain why a change is justified
4. update the decision log if direction intentionally changes

Do not silently overwrite previous decisions.

---

## Validation

Before substantial work is considered complete, verify:

- does it follow `AGENTS.md`?
- does it fit `ROADMAP.md`?
- does it respect `docs/DECISIONS.md`?
- is `docs/PROGRESS.md` accurate?
- does the current lab remain self-contained?
- did we accidentally automate away a learning step?
- did we introduce unexplained concepts?
- did we introduce unnecessary complexity?

---

## Coding principles

Prefer:

- readable code
- small changes
- explicit behavior
- deterministic fault injection
- reproducible examples

Avoid unnecessary abstractions.

The goal is observability learning, not application-framework sophistication.

---

## Current priority

Finish and validate the current lab before starting the next one.

Check `docs/PROGRESS.md` for the exact current state.
