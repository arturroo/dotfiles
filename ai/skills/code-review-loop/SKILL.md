---
name: code-review-loop
description: >-
  Autonomous iterative code review and remediation loop. Orchestrates parallel
  subagents executing fullstack-de-ml-code-review and security-code-review, aggregates
  P0/P1 issues, applies automated fixes, and repeats until all P0 and P1 issues are
  fully resolved (max 5 iterations), surfacing remaining P2/P3 items for user decision.
author: Artur Fejklowicz
copyright: "Copyright (c) 2026 Artur Fejklowicz"
license: Apache-2.0
version: 1.0.0
updated_at: 2026-11-09
---

# Autonomous Code Review & Remediation Loop (`code-review-loop`)

## Overview
This skill executes an autonomous, closed-loop convergence cycle for code quality, architectural integrity, and security hardening. It pairs two independent, complementary review disciplines:
1. **Fullstack, Data Engineering & Cloud Infrastructure Review** (`fullstack-de-ml-code-review`)
2. **Adversarial Red-Team & Zero-Trust Security Audit** (`security-code-review`)

The agent coordinates parallel subagents, aggregates findings, fixes all **P0 (Blockers)** and **P1 (Critical Priority)** defects automatically, and re-reviews iteratively until the codebase reaches 100% P0/P1-clean convergence (or hits the 5-iteration circuit breaker).

---

## Convergence Loop Algorithm

```
                 ┌────────────────────────────────┐
                 │ Initialize: P1 = 1, cnt = 0    │
                 └───────────────┬────────────────┘
                                 │
                 ┌───────────────▼────────────────┐
       ┌─────────► while (P0 + P1 > 0):           │
       │         │   cnt += 1                     │
       │         │   if cnt > 5: break            │
       │         └───────────────┬────────────────┘
       │                         │
       │         ┌───────────────▼────────────────┐
       │         │ Launch Async Subagent 1:       │
       │         │   /fullstack-de-ml-code-review │
       │         │ Launch Async Subagent 2:       │
       │         │   /security-code-review        │
       │         └───────────────┬────────────────┘
       │                         │
       │         ┌───────────────▼────────────────┐
       │         │ Reactive Wait (No Polling)     │
       │         │ Await completion messages      │
       │         └───────────────┬────────────────┘
       │                         │
       │         ┌───────────────▼────────────────┐
       │         │ Parse Reports & Count Severities│
       │         │ Sum unique P0 and P1 issues    │
       │         └───────────────┬────────────────┘
       │                         │
       │                 [P0 + P1 > 0 ?]
       │                 /             \
       │           YES  /               \  NO (Converged!)
       │               v                 v
       │   ┌─────────────────────┐   ┌───────────────────────────┐
       │   │ Print P0/P1 to User │   │ Exit Loop                 │
       │   │ Remediate in Code   │   │ Report 0 P0/P1 status     │
       │   │ Run Tests & Build   │   │ Present remaining P2/P3   │
       │   │ Commit Fixes        │   └───────────────────────────┘
       └───┴─────────────────────┘
```

---

## Detailed Step-by-Step Procedure

### Step 1: Loop Initialization
Initialize loop control state:
- `cnt = 0` (iteration counter)
- `P0 = 0`
- `P1 = 1` (seed condition to enter the loop)
- Max allowed iterations = 5

### Step 2: Parallel Subagent Invocation
In each iteration, launch two dedicated, orthogonal subagents using `invoke_subagent`:

1. **Subagent 1: Fullstack & Architecture Reviewer**
   - **Role:** `Fullstack Code Reviewer`
   - **Type:** `self` (inherits workspace & tools)
   - **Task:** Execute skill `/fullstack-de-ml-code-review` on current branch against `origin/main`.
   - **Output Target:** `tasks/<task_dir>/code_review/fullstack_review_YYYYMMDDHHmmss.md`

2. **Subagent 2: Security & Zero-Trust Auditor**
   - **Role:** `Security Code Reviewer`
   - **Type:** `self` (inherits workspace & tools)
   - **Task:** Execute skill `/security-code-review` on current branch against `origin/main`.
   - **Output Target:** `tasks/<task_dir>/code_review/security_review_YYYYMMDDHHmmss.md`

### Step 3: Reactive Synchronization (Zero-Polling)
- Do **NOT** poll subagent status in a tight loop.
- Stop calling tools and let the reactive agent runtime wake you up upon receiving completion messages from both subagents.

### Step 4: Finding Aggregation & Severity Categorization
Read both generated review reports and parse findings into standardized severity tiers:
- **P0 (Blocker):** Broken core functionality, data corruption, unauthorized data access, privilege escalation, unhandled exceptions crashing endpoints, breaking firestore security rules.
- **P1 (Critical Priority):** Schema mismatches, bypassed App Check / Auth headers, silent query misses, data contract drift, broken routing or UI state mismatches.
- **P2 (Major Priority):** Non-blocking architectural improvements, overly broad IAM permissions, missing secondary cleanups, non-critical performance bottlenecks.
- **P3 (Minor / Defense-in-Depth):** Formatting, log masking, input regex tightening, toast/modal copy improvements, optional documentation polish.

### Step 5: Automated Remediation Gate (When P0 + P1 > 0)
1. **Print P0 & P1 Findings:** Output a structured markdown table / list displaying every identified P0 and P1 issue (file, line number, problem description, required fix).
2. **Apply Code Fixes:**
   - Modify application source files, schemas, and configurations.
   - **Firestore Security Rules Rule:** Whenever `firebase/firestore.rules` must be authored or modified, **MUST** delegate rule authoring to the `firestore-rules-author` subagent rather than editing rules directly.
3. **Run Verification Suite:**
   - Execute Python unit and integration tests: `uv run pytest python_packages/tests/ -v`.
   - Execute frontend production build: `npm --prefix <app_dir> run build`.
   - Execute linters if configured: `npm run lint` / `ruff check`.
4. **Git Stage & Commit:**
   - Stage all modified files and review reports.
   - Commit changes following Conventional Commits (`fix(...): remediate P0 and P1 issues from security and fullstack code reviews`).

### Step 6: Loop Repeat or Termination
- If `P0 + P1 > 0` and `cnt < 5`: Return to Step 2 for the next iteration.
- If `cnt >= 5`: Break loop and alert user that max iterations were reached.
- If `P0 + P1 == 0`: Loop successfully terminates! Proceed to Final Handover.

### Step 7: Final Handover & Remaining Issues Presentation
When the loop finishes:
1. Announce the successful resolution of all P0 and P1 issues (`P0 = 0, P1 = 0`).
2. Clearly list all remaining **P2 (Major)** and **P3 (Minor)** issues with exact file links, descriptions, and actionable decision options so the user can choose whether to fix them immediately or track them in the backlog.
