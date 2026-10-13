<!-- Source: https://www.industrialempathy.com/posts/design-docs-at-google/ -->
<!-- Based on: Google Design Docs structure by Malte Ubl -->
<!-- Adapted as a Technical PRD for AI-assisted implementation workflows -->

---
status: "{draft | in-review | approved | superseded by PRD-NNNN}"
date: {YYYY-MM-DD when the document was last updated}
author: {name, email}
reviewers: {list of reviewers}
adr: {link to the ADR this PRD implements}
---

# {Title: concise name of the feature/system}

## Context and Scope

{Provide a brief overview of the landscape in which the system is being built. What exists today? What is actually being built? Keep it succinct -- assume some prior knowledge and link to detailed background. Focus on objective facts. Reference the ADR for architectural decisions already made.}

## Goals and Non-Goals

### Goals

* {goal 1}
* {goal 2}
* ...

### Non-Goals

* {non-goal 1 -- something that could reasonably be a goal but is explicitly excluded}
* {non-goal 2}
* ...

## The Design

### System Overview

{High-level overview of the solution. Include a system-context-diagram if helpful. Show how this system fits into the broader technical landscape.}

### API Design

{Sketch out APIs the system exposes. Focus on parts relevant to design trade-offs, not verbose formal definitions. Include request/response shapes, endpoints, or function signatures as appropriate.}

### Data Model / Storage

{Describe how and in what form data is stored. Focus on schema elements relevant to design trade-offs. Include entity relationships where helpful.}

### Core Logic / Algorithms

{Describe the key processing logic. Use pseudo-code only for novel algorithms. Link to prototypes if available.}

### Infrastructure / Deployment

{GCP services used, deployment topology, environments, scaling approach, IaC references.}

## Cross-Cutting Concerns

### Security

{Authentication, authorization, data encryption, secrets management.}

### Observability

{Logging, monitoring, alerting, tracing, SLOs.}

### Privacy / Compliance

{Data classification, retention, GDPR/regulatory requirements.}

### Error Handling / Resilience

{Failure modes, retry strategies, circuit breakers, fallback behavior.}

### Performance / Scalability

{Expected load, latency targets, scaling strategy, bottlenecks.}

## Edge Cases and Constraints

### Edge Cases

* {edge case 1 -- boundary condition, unusual input, race condition, etc.}
* {edge case 2}
* ...

### Constraints

* {constraint 1 -- technical limitation, regulatory, budget, timeline, team capacity, etc.}
* {constraint 2}
* ...

## Implementation Plan

### Phases / Milestones

| Phase | Scope | Deliverable | Estimate |
|-------|-------|-------------|----------|
| 1     | {scope} | {deliverable} | {estimate} |
| 2     | {scope} | {deliverable} | {estimate} |

### Dependencies

* {dependency 1 -- team, service, or external system}
* {dependency 2}

### Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| {risk} | {H/M/L} | {H/M/L} | {mitigation} |

## Success Criteria

* {measurable criterion 1}
* {measurable criterion 2}
* ...

## Open Questions

* {question 1 -- to be resolved before/during implementation}
* {question 2}

---

## Implementation Spec

> This section is consumed by the AI coding agent executing `/implement` against this PRD.

### File Structure

{Specify the target directory layout, module boundaries, and naming conventions.}

### Technology Stack

{List exact languages, frameworks, libraries, and versions to use.}

### Coding Standards

{Reference the project's AGENTS.md and any additional style/lint rules. Specify test frameworks and coverage expectations.}

### Step-by-Step Implementation Order

1. {First thing to implement -- e.g., data model / schema}
2. {Second -- e.g., core business logic}
3. {Third -- e.g., API layer}
4. {Fourth -- e.g., infrastructure / IaC}
5. {Fifth -- e.g., tests}
6. {Sixth -- e.g., observability / monitoring}

### Acceptance Criteria (Testable)

* [ ] {criterion 1 -- specific, verifiable}
* [ ] {criterion 2}
* [ ] {criterion 3}
* ...

### Out-of-Scope for Agent (Human Required)

* {item requiring human review/approval -- e.g., IAM role grants in production}
* {item requiring manual step -- e.g., DNS configuration}
