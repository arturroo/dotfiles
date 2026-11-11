---
name: security-code-review
description: >-
  Performs a comprehensive, multi-layered Principal Application, Cloud, Data
  Engineering, and ML/GenAI Security Code Review on a Git branch or diff against
  main. Use when the user asks for a security code review, security audit,
  threat modeling of changes, or pre-PR vulnerability assessment across
  Fullstack (React/Next.js/Firebase), GCP Serverless (Cloud Run/Functions/Terraform),
  Data Engineering (BigQuery/Firestore/Pipelines), or AI/ML (Vertex AI/Gemini).
author: Artur Fejklowicz
copyright: "Copyright (c) 2026 Artur Fejklowicz"
license: Apache-2.0
version: 1.0.0
updated_at: 2026-11-05
---

# Principal Security Code Review (`security-code-review`)

## Overview
This skill executes a rigorous, defense-in-depth security audit of code changes (typically current branch vs. `main`). It combines universal Zero-Trust engineering principles with modular, on-demand domain checklists (**Progressive Disclosure**) covering **Fullstack Web & Cloud**, **Data Engineering (GCP/BigQuery/Firestore)**, and **Machine Learning / GenAI (Vertex AI / Gemini 3.5+)**.

## Strict Operational Posture (Read-Only Audit Rule)
- **Audit First, Never Mutate Unprompted:** During a security code review, operate strictly as a **read-only auditor**. Do NOT modify application code, Terraform configs, or dependencies unless the user explicitly asks you to implement fixes in the current session.
- **Exception:** Writing or updating the security review report file (`<task_dir>/code_review/security_review_YYYYMMDDHHmmss.md`, e.g. `security_review_20261105174132.md`) is permitted and expected when requested.

---

## Workflow Steps

### Step 1: Pre-Flight Reconnaissance & Diff Classification
1. Identify the active branch and inspect changes against the base branch (`main`):
   - `git status --short`
   - `git log main..HEAD --oneline`
   - `git diff main...HEAD --stat`
2. Read the repository's `GEMINI.md` (and any relevant directory `GEMINI.md` or `ADR.md`/`PRD.md` in `tasks/`) to establish the **immutable architectural and security baseline**.
3. Classify the modified files into one or more security domains to determine which reference checklists to load in Step 2:
   - **Domain A — Fullstack Web, API & Cloud Native:** Next.js / React (`src/`, `app/`), Firebase Hosting/Storage/Firestore rules, Cloud Functions / Cloud Run HTTP endpoints, OIDC / Firebase Auth / App Check, email/HTML rendering, SEO metadata (`JSON-LD`).
   - **Domain B — Data Engineering & ML / GenAI:** BigQuery (`bq`), SQL/NoSQL queries, ETL/ELT pipelines, Eventarc / Pub/Sub triggers, Vertex AI / Gemini SDK (`google-genai`), prompt engineering / RAG / Google Search grounding, Pydantic schemas, Python packages (`pyproject.toml`).
   - **Domain C — Infrastructure as Code (Terraform & CI/CD):** `terraform/*.tf`, IAM bindings, service accounts, Secret Manager, GitHub Actions workflows.

### Step 2: Progressive Disclosure — Load Domain Checklists
To optimize context window efficiency while maintaining deep domain rigor, read **only** the reference manuals matching the domains touched by the diff:
- If **Domain A** or **Domain C** is touched -> Read [fullstack-web-cloud.md](./references/fullstack-web-cloud.md).
- If **Domain B** or **Domain C** is touched -> Read [data-engineering-ml-ai.md](./references/data-engineering-ml-ai.md).
- *(Note: For hybrid diffs—such as a Cloud Function running Gemini trend analysis and saving to Firestore for a React CMS—load **both** reference files).*
- If `firestore.rules` or `storage.rules` are modified -> Also apply the `firebase-security-rules-auditor` skill checklist if available.

### Step 3: Universal Core Security Gates (Always Enforced)
Regardless of domain, evaluate every modified file against these four mandatory gates:

1. **Multi-Layered Defense-in-Depth & Fail-Fast Gatekeeping:**
   - **Layer 1 (Entry Gatekeeper):** Every external or cross-service input (HTTP body, query params, path params, Eventarc headers, webhook payloads, LLM/trend inputs) MUST be strictly validated at the entry boundary (Pydantic `Field(min_length=..., max_length=..., pattern=...)`, `Literal` enums, strict type checking).
   - **Fail-Fast Rejection:** If any parameter contains unexpected HTML/script tags (`<`, `>`), control characters (`\r`, `\n`, `\x00`), path traversal sequences (`..`, `/`, `\`), or exceeds length bounds, the service MUST immediately stop and raise an actionable HTTP `400`/`422` validation error—never silently truncate or sanitize-and-continue on malformed identity/control fields.
   - **Layer 2 (Context-Aware Encoding):** Apply `html.escape(..., quote=True)` for HTML body/attributes/titles, `.replace(/</g, '\\u003c')` for `<script type="application/ld+json">`, and parameterized queries for SQL/BigQuery.
   - **Layer 3 (Client/Execution Isolation):** Isolate untrusted or template HTML in `<iframe sandbox="" srcDoc={...} />` rather than raw `dangerouslySetInnerHTML`.

2. **Zero-Trust Authentication & Authorization (No Spoofable Headers):**
   - Never trust plain HTTP headers (`X-CloudScheduler`, `User-Agent`, `X-Forwarded-For`) for authorization when a service is reachable via `allUsers` or a reverse proxy.
   - Require cryptographic token verification:
     - **User/Admin Requests:** `firebase_admin.auth.verify_id_token(token)` + RBAC custom claim check (`decoded.get("admin") is True`) + `firebase_admin.app_check.verify_token()`.
     - **Service-to-Service / Cron:** `google.oauth2.id_token.verify_oauth2_token(token, Request(), audience=...)` with explicit verification of `email_verified` and an exact allowlist of project Service Account emails (never generic suffix matching like `.endswith('-compute@developer.gserviceaccount.com')` across all GCP projects).
   - Never use exception message substring matching (e.g., `"iss" in str(e)`) to bypass cryptographic verification failures.

3. **Supply Chain & Python Packaging Hygiene (Cloud Functions Gen 2 / Cloud Run):**
   - Python services and Cloud Functions Gen 2 MUST define dependencies exclusively in `pyproject.toml` with **exact pinned versions** (`==`, no `^` or `>=`).
   - Flag dual dependency files (`requirements.txt` alongside `pyproject.toml`) as a **Supply-Chain Drift Risk** because Google Cloud Buildpacks prioritize `requirements.txt` and silently ignore `pyproject.toml`.
   - In Terraform `archive_file` data sources, verify the standard exclusion list (`[".git", ".venv", "__pycache__", ".pytest_cache", ".zips", "zips", ".gemini", "node_modules", ".DS_Store"]`) is present.

4. **Actionable Error Handling Without Information Disclosure:**
   - Verify errors follow the Actionable Errors standard (what failed, whom to contact, concrete workaround) **without** leaking raw Python stack traces, internal SQL/Firestore paths, Secret Manager resource names, or PII to public clients.

### Step 4: Subagent Execution Strategy (2026 Best Practices)
- **Direct Execution:** When the user asks for a security review in the current session, execute Steps 1–5 directly.
- **Delegated Subagent Execution:** When invoked as part of a larger implementation workflow or multi-agent team (`/teamwork` or `invoke_subagent`), launch a dedicated read-only `research` subagent (or `self` subagent if write access to `code_review/security_review_YYYYMMDDHHmmss.md` is needed) with:
  - Isolated context focused purely on the diff and target files.
  - Adversarial "Red Team" mindset: trace data flow from **Untrusted Source -> Validation Boundary -> Storage/LLM Sink -> Render/Execution Sink**.
  - Zero tolerance for false positives: every reported finding must cite exact file paths, line numbers, a concrete exploit scenario, and a drop-in remediation snippet.

### Step 5: Report Generation & Context Feedback Loop
1. Format the review using [report-template.md](./resources/report-template.md).
2. Always write the report file in **English** (while conversing with the user in their preferred language, e.g., Polish).
3. When saving to disk, format the filename strictly with the compact technical timestamp: `<task_dir>/code_review/security_review_YYYYMMDDHHmmss.md` (e.g. `security_review_20261105174132.md`):
   - Use **relative repository links** inside the saved markdown file (e.g., `[main.py](../../../../cloud_functions/cf-name/main.py#L45-L60)`) so no local machine paths (`file:///c:/Users/...`) leak to GitHub.
   - Include a **Proposed Input Validation Matrix** for all modified endpoints/forms/schemas.
   - Include a **Proposed `GEMINI.md` Rules Update** section if the review uncovered systemic architectural patterns that should be codified globally or at the repo level.
