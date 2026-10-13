---
author: Artur Fejklowicz
copyright: "Copyright (c) 2026 Artur Fejklowicz"
license: Apache-2.0
version: 1.0.0
updated_at: 2026-10-14
---

# Minimalist Terraform Standards for Google Cloud

These standards outline clean, secure, and maintainable Infrastructure as Code (IaC) using Terraform on Google Cloud.

---

## 1. Provider & Version Constraints

- **Google Cloud Provider:** Pin provider version to `~> 7.0`:
  ```hcl
  terraform {
    required_version = ">= 1.9.0"
    required_providers {
      google = {
        source  = "hashicorp/google"
        version = "~> 7.0"
      }
    }
  }
  ```

---

## 2. Remote State Management (GCS Backend)

- **Strict GCS Remote State:** Never store or commit local state (`terraform.tfstate`).
- **Configuration (`backend.tf`):**
  ```hcl
  terraform {
    backend "gcs" {
      bucket = "af-terraform-state"
      prefix = "infrastructure/state"
    }
  }
  ```
- **State Locking & Encryption:** Handled natively by GCS. Ensure versioning is enabled on the state bucket.

---

## 3. Directory Layout & Module Structure

Keep configurations clean and modular:
```text
terraform/
├── backend.tf       # Remote state declaration
├── main.tf          # Core resources and provider configurations
├── variables.tf     # Explicitly typed variables with descriptions
├── outputs.tf       # Exported resource IDs, endpoints, and identities
└── modules/         # Reusable modules (cloud_run, bigquery, etc.)
```

---

## 4. Resource Naming & Identity Hygiene

- **Resource Naming:** All resources must follow kebab-case with resource-type prefixes (`cr-`, `bq-`, `fs-`).
- **Service Accounts:**
  - Standard format: `sa-{resource_short}-{name}`
  - Maximum 30 characters:
  ```hcl
  resource "google_service_account" "sa" {
    account_id   = "sa-cr-mcp-workspace"
    display_name = "Service Account for MCP Workspace"
  }
  ```

---

## 5. Secret Management in Terraform

- **Zero Hardcoded Secrets in HCL:**
  - Never put API keys, passwords, or bearer tokens in `.tf` or `.tfvars` files.
  - Reference secrets dynamically from GCP Secret Manager:
  ```hcl
  # Mount secret as environment variable in Cloud Run
  env {
    name = "APP_API_KEY"
    value_source {
      secret_key_ref {
        secret  = "APP_API_KEY"
        version = "latest"
      }
    }
  }
  ```
- **Secret Verification Pre-Flight:**
  - Before applying Terraform that binds secrets, always verify their physical existence in Secret Manager:
    ```powershell
    gcloud secrets list
    ```
