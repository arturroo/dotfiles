---
name: fullstack-de-ml-code-review
description: >-
  Performs a deep, multi-disciplinary Google Staff/Principal Code Review across
  Fullstack Engineering (React/Next.js, Python APIs, Cloud Run/Functions Gen 2,
  Firebase, Terraform IaC), Data Engineering (BigQuery, Firestore, Eventarc,
  Pub/Sub, ETL/ELT, Dataform/dbt), and Machine Learning / GenAI (Vertex AI,
  Gemini 3.5+/3.8 Thinking, Grounding, RAG, Pydantic schemas, MLOps). Use when
  the user asks for a fullstack, data engineering, ML/AI, or architectural code
  review of a branch or diff against main.
author: Artur Fejklowicz
copyright: "Copyright (c) 2026 Artur Fejklowicz"
license: Apache-2.0
version: 1.0.0
updated_at: 2026-11-05
---

# Principal Fullstack, Data Engineering & ML/GenAI Code Review (`fullstack-de-ml-code-review`)

## Overview
This skill executes a production-grade engineering and architectural code review of a Git branch or diff (typically against `main`). It is designed to work as the **Engineering & Architecture counterpart** to `security-code-review`: while `security-code-review` focuses on adversarial threat modeling and CWE vulnerabilities, `fullstack-de-ml-code-review` focuses on **end-to-end data contract integrity, runtime correctness, cloud-native IaC parity, BigQuery/Firestore data engineering best practices, and ML/GenAI system reliability**.

It uses **Progressive Disclosure** (`references/`) so that pure Fullstack, pure Data Engineering/ML, and hybrid AI-Fullstack repositories each load only the checklists they need while preserving 100% visibility across cross-domain boundaries.

## Strict Operational Posture (Read-Only Reviewer Rule)
- **Review First, Never Mutate Unprompted:** During a code review, operate strictly as a **read-only reviewer**. Do NOT modify application code, schemas, pipelines, or Terraform configurations unless the user explicitly instructs you to apply the fixes.
- **Exception:** Creating or updating the markdown review artifact on disk (e.g., `<task_dir>/code_review/fullstack_review_YYYYMMDDHHmmss.md`) is permitted and expected when requested.

---

## Workflow Steps

### Step 1: Pre-Flight Reconnaissance & Cross-Boundary Diff Mapping
1. Inspect the active branch state and diff against `main` (or `origin/main`):
   - `git status --short`
   - `git log origin/main..HEAD --oneline`
   - `git diff origin/main...HEAD --stat`
2. Read the repository's `GEMINI.md` (plus any component `GEMINI.md` and task `BRD.md` / `ADR.md` / `PRD.md`) to establish the **immutable architectural baseline**.
3. Classify the diff across the three engineering pillars to select which reference checklists to load in Step 2:
   - **Pillar 1 — Fullstack Web, APIs & Cloud Infrastructure:** React / Next.js (`app/`, `src/`), state management, SSR/ISR caching, SEO & `JSON-LD`, Cloud Functions Gen 2 / Cloud Run microservices, Firebase (Firestore/Storage/Auth/Hosting), and Terraform (`terraform/*.tf`).
   - **Pillar 2 — Data Engineering & Event-Driven Pipelines:** BigQuery (`bq`) SQL/DDL/DML, partitioning/clustering, Firestore data modeling & batch/transaction semantics, Eventarc / Pub/Sub / Cloud Scheduler orchestration, idempotency, schema evolution, and Python packaging (`uv`, `pyproject.toml`).
   - **Pillar 3 — Machine Learning, MLOps & GenAI Systems:** Vertex AI, Gemini 3.5+ / 3.8 Thinking models (`google-genai`), Google Search Grounding, RAG / embeddings, prompt materialization (`ai_prompts`), Pydantic structured outputs (`response_schema`), evaluation guards, and training/inference feature parity.

### Step 2: Progressive Disclosure — Load Domain Checklists
Load only the reference checklists matching the pillars touched by the diff:
- If **Pillar 1** is touched -> Read [fullstack-web-cloud-iac.md](./references/fullstack-web-cloud-iac.md).
- If **Pillar 2** or **Pillar 3** is touched -> Read [data-engineering-ml-genai.md](./references/data-engineering-ml-genai.md).
- *(Note: For vertical AI features—e.g., a Gemini/BigQuery backend feeding a Firestore collection rendered by a React/Next.js UI—load **both** checklists so cross-boundary contracts are verified end-to-end).*

### Step 3: The 5 Universal Cross-Boundary Gates (Always Enforced)
Over 80% of P0 production bugs occur at the seams between systems. Regardless of domain, audit every diff against these five mandatory gates:

1. **End-to-End Data Contract Parity (Producer ↔ Storage ↔ Consumer):**
   - Trace every field name, nesting level, and type across the full lifecycle:
     - **AI / Pipeline Producer** (Pydantic `BaseModel`, BigQuery table schema, seed script)
     - **Storage Layer** (Firestore document structure, BigQuery table/view, GCS object path)
     - **UI / Downstream Consumer** (Next.js SSR data loader, React form state, BI dashboard, downstream ML model)
   - Flag any key mismatch (e.g., producer writes `shop_header_title` while consumer reads `title`) or partial state overwrite (e.g., loading a partial AI draft into React state without merging existing document keys) as a **Severity 1 (P0) Blocker**.

2. **Code ↔ Infrastructure (Terraform / IAM / Triggers) Parity:**
   - For every Cloud Function Gen 2, Cloud Run service, or pipeline job modified in code, cross-check `terraform/` (`variables.tf`, `main.tf`):
     - Does the Service Account have every required IAM role (e.g., `roles/aiplatform.user` for Vertex AI/Gemini, `roles/datastore.user` for Firestore, `roles/bigquery.dataEditor` / `jobUser` for BigQuery)?
     - Do Eventarc / Pub/Sub / Scheduler triggers match the exact collection/document path or topic expected by the code (e.g., `document = "collection/{docId}"`)?
     - Are all environment variables and Secret Manager bindings declared in Terraform?

3. **Python Packaging & Runtime Dependency Integrity (`pyproject.toml` Only):**
   - Verify all Cloud Functions (`GEN_2`), Cloud Run services, and Python packages manage dependencies **exclusively via `pyproject.toml`** with exact `==` pinned versions (no `^` or `~`).
   - Flag any `requirements.txt` in a Cloud Function Gen 2 directory (either standalone or alongside `pyproject.toml`), as Google Cloud Buildpacks prioritize `requirements.txt` and bypass `pyproject.toml` private Artifact Registry indices.
   - Verify all implicit runtime extras are explicitly pinned (e.g., `email-validator==...` whenever `pydantic.EmailStr` is imported).

4. **Actionable Error Handling & Observability Standard:**
   - Verify no errors are silently swallowed (`catch (_) {}` or bare `except: pass`) and no false-positive success toasts/logs are emitted on failure.
   - Every user-facing or CLI/pipeline error must state: (1) what specifically failed and why, (2) whom to contact or where to inspect logs (e.g., *"Skontaktuj się z Arturem"*), and (3) a concrete workaround or next step.

5. **Baseline & Domain Policy Compliance (`GEMINI.md`):**
   - Verify strict compliance with all rules in global and project `GEMINI.md` (e.g., Gemini 3.5+ / 3.8 Thinking models with `thinking_level` in `types.ThinkingConfig`, Brand Manifesto & LSI/E-E-A-T copywriting rules, outbound customer communication language policy, timezone-aware `datetime.now(timezone.utc)`).

### Step 4: Subagent Orchestration Strategy (2026 Best Practices)
- **Small-to-Medium Diffs (<= 20 files):** Execute the review directly in the main agent after reading the relevant `references/` files.
- **Large Multi-Domain Diffs (> 20 files) or `/teamwork` Mode:** You may fan out parallel read-only `research` subagents with orthogonal scopes:
  - *Subagent 1 (Backend, Cloud IaC & Security Boundary):* Audits Python Cloud Functions/Run, `pyproject.toml`, `terraform/`, IAM, and auth verification.
  - *Subagent 2 (Data Engineering, Schemas & ML/GenAI):* Audits BigQuery/Firestore data models, idempotency, `florka_ai` / Vertex AI Gemini prompts, `ThinkingConfig`, and Pydantic schemas.
  - *Subagent 3 (Frontend Architecture, UX & Data Contracts):* Audits React/Next.js components, SSR/ISR caching, state merging, mobile UX standards, and Producer-to-UI field parity.
  - Synthesize subagent findings in the primary agent, deduplicating overlapping issues and verifying every cited line number before generating the final report.

### Step 5: Report Generation & Self-Improving Context Loop
1. Structure the output following [report-template.md](./resources/report-template.md).
2. Always write the saved markdown file in **English** (while replying in chat in the user's preferred language, e.g., Polish).
3. When saving to disk, format the filename strictly with the compact technical timestamp: `<task_dir>/code_review/fullstack_review_YYYYMMDDHHmmss.md` (e.g. `fullstack_review_20261105173908.md`):
   - Use **strictly relative repository links** (e.g., `[main.py](../../../../cloud_functions/cf-name/main.py#L64-L108)`) so local filesystem paths (`file:///c:/Users/...`) never leak to Git.
4. **Self-Improving `GEMINI.md` Loop:** At the end of every review, evaluate whether any discovered bug represents a recurring architectural pattern across Fullstack, Data Engineering, or ML/AI. If so, include a **Recommended Additions to `GEMINI.md`** section with copy-pasteable rules for Global (`~/.gemini/GEMINI.md`) and/or Project `GEMINI.md`.
