---
author: Artur Fejklowicz
copyright: "Copyright (c) 2026 Artur Fejklowicz"
license: Apache-2.0
version: 1.0.0
updated_at: 2026-10-14
---

# Google Cloud Architecture Standards

These standards govern resource architecture, identity management, and serverless deployments across Google Cloud Platform (GCP).

---

## 1. Naming Conventions & Global Scoping

To avoid global namespace collisions (especially with GCP Projects, Google Cloud Storage buckets, and Artifact Registry repositories):
- **Universal Project / Resource Prefix:** `af-` (Artur Fejklowicz signature prefix, preventing global resource collision).
- **Format:** `af-{domain/project}-{resource}`
  - Example Bucket: `gs://af-analytics-workspaces`
  - Example Artifact Registry: `af-docker-repo`

### Resource Type Prefixes
Resource names follow a strict kebab-case format with functional prefixes:
* `bq-` — BigQuery datasets and routines (e.g. `bq-telemetry`)
* `fs-` — Firestore databases/collections
* `cr-` — Cloud Run microservices (e.g. `cr-mcp-workspace`)
* `cf-` — Cloud Functions (entrypoint is always `main()`)
* `sm-` — Secret Manager secrets (UPPER_SNAKE_CASE in Secret Manager, e.g. `APP_API_KEY`)
* `sa-` — Service Accounts (see identity section below)

---

## 2. Identity & Access Management (IAM)

- **Service Account Naming:**
  - Prefix pattern: `sa-{resource_type_short}-{name}` (e.g. `sa-cr-mcp-workspace`).
  - Maximum length: 30 characters (GCP constraint).
- **Service Account Keys:**
  - **Never generate or commit service account JSON key files (`*.json`).**
  - Use Workload Identity Federation or default compute identities.
- **Local Authentication:**
  - Authenticate locally using Application Default Credentials (ADC):
    ```powershell
    gcloud auth application-default login
    ```
  - Keep `$env:GOOGLE_APPLICATION_CREDENTIALS` unset locally to prevent accidental conflict with service account files.

---

## 3. Cloud Run Stateless Microservices

- **Container Statelessness & Zero Disk Poisoning:**
  - Cloud Run instances must remain 100% stateless.
  - Never write agent scratch buffers or staged data to local container storage (`workspace/`), as local files get accidentally baked into Docker images via `COPY . .`.
- **Mandatory Endpoints:**
  - Every microservice must expose `@app.get("/health")` and `@app.get("/")`.
- **Private Microservice Invocation (PowerShell):**
  - Services are deployed private (`public = false`), requiring OIDC tokens:
    ```powershell
    $token = $(gcloud auth print-identity-token)
    curl.exe -s -H "Authorization: Bearer $token" "https://<service-url>/health"
    ```
- **Container Build Scaffolding:**
  - `.dockerignore` and `.gcloudignore` must strictly exclude `.git`, `.venv`, `__pycache__`, `*.pyc`, `.env`, and tests to prevent Cross-Platform Venv Poisoning (Windows `.exe` binaries breaking in Linux containers).

---

## 4. Secret Manager & Environment Configuration

- **Zero Hardcoded Endpoints:**
  - API URLs, tokens, and keys must never be hardcoded in application code.
  - Store all production secrets in GCP Secret Manager.
  - Safely read environment variables with fallback protection:
    ```python
    import os
    API_URL = os.getenv("API_URL") or "https://fallback.internal"
    ```
