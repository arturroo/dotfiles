---
name: create-adr
description: >-
  Runs an interactive, tiered Socratic process (with pre-flight codebase reconnaissance, GEMINI.md baseline, archetypal MCQ options, and on-demand Expert Matrix), then generates ADR.md in MADR Compound format. Requires BRD.md to exist.
---

# Create ADR (Architecture Decision Record)

## Overview
This skill guides the architecture and design phase of a task using a focused, multi-turn Socratic decision tree. It performs a quick reconnaissance of recent projects in the repo, treats `GEMINI.md` as the immutable baseline, asks targeted multiple-choice questions structured around industry archetypes, supports deep-dive expert evaluations on demand, and generates `ADR.md` based on the MADR Compound template.

## Requirements
- **Prerequisite**: A `BRD.md` file MUST exist in the target task folder. If it does not exist, fail immediately and request the user to create or provide a `BRD.md`. Do not start without it.

## Socratic Process & Architectural Baseline

### 1. Quick Codebase Reconnaissance (Recent Precedents & Patterns)
Before formulating questions, perform a brief, targeted reconnaissance of the repository:
- Inspect 1-2 most recently completed projects, tasks, or modules in the codebase (e.g. sibling folders, recent git history, or previous PRDs/ADRs).
- Quickly observe established conventions: project structure, shared packages/libraries, configuration loading, schema patterns, and recent architectural precedents.
- Use these insights to ground your questions in actual codebase reality, avoiding questions that have already been settled by precedent.

### 2. Architectural Baseline & Framing
The following GCP standards and project rules from `GEMINI.md` (or repository architectural guidance) serve as the framing for the Technical Specifications section of the generated ADR:
1. **Infrastructure**: Terraform is the standard for Infrastructure as Code (IaC). Use Google Provider `~> 7.0` and store state remotely (GCS) when applicable. Naming conventions are kebab-case with resource-type prefix (e.g. `bq-dataset-name`, `sa-name`, `cf-name`).
2. **GCP Serverless**: Default to BigQuery (`bq`), Firestore (`fs`), and Cloud Run. Cloud Functions entry point must be `main()`.
3. **Billing/Cost**: Prioritize cost optimizations and free tiers for small-to-medium scale prototyping.
4. **Security**: Simple security/rules for prototyping or lessons, but Service Accounts (`sa-{resource_type_short}-{name}`) and JWT for production setups.
5. **Python Standards**: Use `uv` package manager, precise library versions, `requires-python = "==3.13.5"`, and `pathlib.Path`.

**RULE**: `GEMINI.md` is the immutable architectural baseline. DO NOT ask the user to choose or confirm any of the baseline standards above (e.g. dual backend LangChain + Google ADK, BigQuery dataset, Cloud Run microservice, Gemini 3.8 Flash) unless an explicit deviation is requested.

### 3. Targeted Questions & Option Archetypes (3-6 Focused Decision Points)
Ask 3-6 targeted multiple-choice questions focusing exclusively on task-specific architectural trade-offs. Present initial questions using the `ask_question` tool (or structured markdown if in a deep-dive turn):

1. **Deviation Check (Always ask this first in Turn 1)**:
   - "Do we adhere 100% to the GEMINI.md architectural baseline or introduce intentional deviations?"
2. **Domain-Specific Architectural Decisions (2-5 questions derived from BRD.md)**:
   - Ask only questions that address real ambiguities or architectural trade-offs in the task (safety/guardrails, autonomous loop vs deterministic pipeline, state management, optional relevant tech like FastMCP/LangGraph).
   - **Tag Reversibility**: Next to each question title, include `[Reversibility: High (Type 2)]` or `[Reversibility: Low (Type 1)]` so Artur knows where to invest deep thinking.
   - **Archetypal Options**: Whenever applicable, structure the multiple-choice options around these three archetypes (placing the `(Recommended)` badge on the best-fit option first):
     - **Option A [Pragmatic / MVP]**: Fastest delivery, minimal boilerplate, leverages existing repo patterns and `GEMINI.md` defaults.
     - **Option B [Industry Best Practice]**: Current standard for long-term maintainability, clean separation of concerns, and testability.
     - **Option C [Google-Scale / Cloud-Native Pattern]**: How Google solves this at scale (e.g. strict statelessness, event-driven choreography, zero-trust/IAM isolation, Google Design Doc patterns).
   - **Exception-Only Red Flags**: Do not write long essays for each option. However, if any option introduces a critical risk (security hole, severe vendor lock-in, or billing trap), append a concise 1-line warning: `🔴 [Security/DataEng/Arch Warning]: <max 12 words>`.

### 4. Interactive Decision Tree & "On-Demand" Expert Matrix
Because initial answers often trigger sub-decisions or require deeper exploration before freezing `ADR.md`, manage the multi-turn conversation using these rules:

- **On-Demand Deep Dive (`?` or `rada`)**: If Artur replies with a question number followed by `?`, `rada`, or asks for more data/expert views on a specific point (e.g., `2?`, `rada do 3`), DO NOT generate `ADR.md` yet. Instead, output a compact **Expert Veto Matrix** for that specific decision:

  | Option | 🛠️ Data Eng (Artur) | 🛡️ Security | 🏛️ Architect |
  | :--- | :--- | :--- | :--- |
  | **A (Pragmatic)** | 🟢/🟡/🔴 *(max 8 words)* | 🟢/🟡/🔴 *(max 8 words)* | 🟢/🟡/🔴 *(max 8 words)* |
  | **B (Best Practice)** | 🟢/🟡/🔴 *(max 8 words)* | 🟢/🟡/🔴 *(max 8 words)* | 🟢/🟡/🔴 *(max 8 words)* |
  | **C (Google Way)** | 🟢/🟡/🔴 *(max 8 words)* | 🟢/🟡/🔴 *(max 8 words)* | 🟢/🟡/🔴 *(max 8 words)* |

  *(Note: Keep user/UX perspective out of the ADR matrix—defer UX ergonomics to the PRD phase unless it directly impacts backend latency/SLAs).*

- **Decision Parking Lot (State Tracking)**: Whenever the conversation branches into follow-up questions or deep dives, append a compact status block at the very bottom of your response so no threads are lost:
  - `✅ Locked Decisions: [brief list of settled points]`
  - `🔄 Active Branch: [current sub-decision being explored]`
  - `⏳ Pending from BRD: [remaining open topics before ADR generation]`

- **Completion Trigger**: Only generate the final `ADR.md` file once all branches in the Decision Parking Lot are resolved (`⏳ Pending` is empty).

## Template
Load and follow the MADR Compound template strictly from:
[madr-compound.md](../templates/madr-compound.md)

## Output, Verification & Context Feedback Loop
- Save the generated file as `ADR.md` in the same directory where `BRD.md` is located.
- The status field in the MADR frontmatter MUST be set to `Proposed`.
- Use strictly relative markdown links inside the document (e.g. `[BRD.md](BRD.md)`, never absolute `file:///` paths) to prevent leaking local usernames and paths to GitHub.
- **Self-Improving Context Check**: After saving `ADR.md`, evaluate if any new, reusable project-wide or directory-wide convention emerged during the Socratic dialogue. If so, propose a 1-2 line snippet for Artur to approve adding to the local `GEMINI.md` or `AGENTS.md`.
- Prompt the user to review the decisions and change the status to `Accepted` before generating the PRD.
