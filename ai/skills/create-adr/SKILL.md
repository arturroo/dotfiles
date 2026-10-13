---
name: create-adr
description: >-
  Runs the Socratic process (with pre-flight codebase reconnaissance, GEMINI.md baseline, and targeted domain questions), then generates ADR.md in MADR Compound format. Requires BRD.md to exist.
---

# Create ADR (Architecture Decision Record)

## Overview
This skill guides the architecture and design phase of a task using a focused Socratic process. It performs a quick reconnaissance of recent projects in the repo, treats `GEMINI.md` as the immutable baseline, asks 3-6 targeted questions (including a mandatory deviation check), and generates `ADR.md` based on the MADR Compound template.

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

### 3. Targeted Questions (3-6 Focused Decision Points)
Ask 3-6 targeted multiple-choice questions focusing exclusively on task-specific architectural trade-offs. Present all questions in a single batch call using the `ask_question` tool with structured options, placing `(Recommended)` as the first option:

1. **Deviation Check (Always ask this first)**:
   - "Do we adhere 100% to the GEMINI.md architectural baseline or introduce intentional deviations?"
2. **Domain-Specific Architectural Decisions (2-5 questions derived from BRD.md)**:
   - Ask only questions that address real ambiguities or architectural trade-offs in the task. If a task is simple, do not fabricate trivial questions just to reach a quota.
   - Specific safety/guardrail mechanisms (e.g. client-side interception, rate limiting, anti-tamper policies).
   - Domain execution strategy (e.g. autonomous agent loop vs deterministic pipeline, error recovery, backoff policies).
   - Optional technologies (e.g. additional FastMCP server, LangGraph, vector search) ONLY if directly relevant to the task.
   - Any critical context needed to understand the task better or edge cases that Artur might want to address.

## Template
Load and follow the MADR Compound template strictly from:
[madr-compound.md](../templates/madr-compound.md)

## Output & Verification
- Save the generated file as `ADR.md` in the same directory where `BRD.md` is located.
- The status field in the MADR frontmatter MUST be set to `Proposed`.
- Use strictly relative markdown links inside the document (e.g. `[BRD.md](BRD.md)`, never absolute `file:///` paths) to prevent leaking local usernames and paths to GitHub.
- Prompt the user to review the decisions and change the status to `Accepted` before generating the PRD.
