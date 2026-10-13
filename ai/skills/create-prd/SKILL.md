---
name: create-prd
description: >-
  Combines BRD.md and an Accepted ADR.md to generate the final PRD.md file in the Google Design Doc format.
author: Artur Fejklowicz
copyright: "Copyright (c) 2026 Artur Fejklowicz"
license: Apache-2.0
version: 1.0.0
updated_at: 2026-10-14
---

# Create PRD (Product Requirements Document)

## Overview
This skill merges the Business Requirements Document (`BRD.md`) and the Architecture Decision Record (`ADR.md`) into a single Technical Product Requirements Document (`PRD.md`). The PRD is an execution document following the Google Design Doc style.

## Requirements
- **Prerequisite**: Both `BRD.md` and `ADR.md` MUST exist in the target task folder.
- **Validation**: Read `ADR.md` and verify the status of the decisions is set to `Accepted`. If the status is `Proposed` or anything else, stop and inform the user that they must review and change the status to `Accepted` first.

## Architectural Baseline Alignment
The PRD MUST strictly align with the accepted `ADR.md` and the `GEMINI.md` project baseline:
- **Dual Framework Standard**: Implement feature parity for both **LangChain 1.2.15** (`create_agent`) and **Google ADK 1.33.0** (`google.adk.Agent`, `Runner`, `InMemorySessionService`) selectable via `--backend [langchain|adk]`. `google-genai` is strictly the underlying model driver, never an alternative agent framework.
- **Cloud Run Microservice Standards**: Endpoints `@app.get("/health")`, `@app.get("/")`, `@app.post("/run")`, and CLI mode `run_cli()` in `main.py`. Standard scaffolding: `.dockerignore`, `.gcloudignore`, `cloudbuild.yaml`, `Dockerfile` with `python:3.13.5-slim`.
- **Telemetry & Storage**: Dedicated BigQuery dataset per service/domain with streaming audit table, and LangSmith tracing.
- **Zero-Hardcoding**: Never include raw external API URLs or secrets; use environment variable placeholders (e.g. `$APP_API_VERIFY`, `$APP_API_SHELL`).

## Scope Boundaries
- **No Alternatives Considered**: Do not include alternatives, rejected options, or justifications for architectural choices in the PRD. The ADR has already closed that discussion.
- Focus strictly on **committed implementation guidance** (how to build it).

## Template
Load and follow the Google Design Doc template strictly from:
[technical-prd.md](../templates/technical-prd.md)

## Implementation Spec
Pay special attention to the **Implementation Spec** section at the bottom of the template. It must be highly detailed and specific for the AI coding agent:
1. **File Structure**: Define exact file names and directories.
2. **Technology Stack**: Specify exact languages, frameworks (**LangChain 1.2.15** and **Google ADK 1.33.0**), libraries, and precise versions in `pyproject.toml` (sorted alphabetically, `requires-python = "==3.13.5"`).
3. **Coding Standards**: Reference project standards (Pydantic contract-first schemas with explicit `description`, `examples`, and `reasoning`/`hint` fields; `pathlib.Path`; `os.getenv("VAR") or "default"`).
4. **Step-by-step Implementation Order**: A logical, dependency-first task breakdown.
5. **Acceptance Criteria**: Testable, checkbox-formatted criteria.
6. **Out-of-Scope**: What requires human interaction/review.

## Output
- Save the document as `PRD.md` in the same directory.
- Use strictly relative markdown links inside the document (e.g. `[ADR.md](ADR.md)`, never absolute `file:///` paths) to prevent leaking local usernames and paths to GitHub.
- Provide the user with a clickable link to the generated file.
