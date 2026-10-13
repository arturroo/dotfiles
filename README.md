# dotfiles

> **Personal dotfiles: AI & engineering standards, developer environments, and architectural (anti)patterns for Data & ML Engineering.**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.13.5-3776AB.svg?logo=python&logoColor=white)](standards/python.md)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-Enterprise_Architecture-4285F4.svg?logo=googlecloud&logoColor=white)](standards/gcp.md)
[![Terraform](https://img.shields.io/badge/Terraform-~>_7.0-844FBA.svg?logo=terraform&logoColor=white)](standards/terraform.md)

---

## Overview

This repository is the central source of truth for developer environment configurations, AI agent workflows, architectural standards, and project scaffolding across personal and professional projects.

Designed for seamless portability between local environments, cloud containers, and **GitHub Codespaces**.

---

## Repository Structure

```text
dotfiles/
├── .gitignore                      # Zero-secret and clean environment ignore rules
├── LICENSE                         # Apache 2.0 License
├── README.md                       # Repository overview and setup guide
│
├── ai/                             # AI & Agentic Engineering
│   ├── instructions/
│   │   └── GEMINI.md               # Universal system prompt & pair-programming instructions
│   └── skills/                     # Reusable agent skills & workflow templates
│       ├── create-adr/             # Architecture Decision Record generator (MADR format)
│       ├── create-brd/             # Business Requirements Document extractor
│       ├── create-prd/             # Product Requirements Document generator
│       ├── implement-prd/          # Specification execution engine
│       ├── git-add-commit-and-push/# Secure audit, stage, commit, and push skill
│       └── templates/              # MADR and technical PRD markdown templates
│
├── standards/                      # Engineering Standards & Architectural Patterns
│   ├── data-engineering.md        # BigQuery partitioning/clustering, Firestore, idempotency
│   ├── gcp.md                     # Resource naming (af-*), IAM, Cloud Run, Secret Manager
│   ├── machine-learning.md        # Vertex AI integrations, model cognitive hierarchy, token economics
│   ├── python.md                  # Python 3.13, uv, Ruff, Mypy, PEP 585/604, Pydantic hygiene
│   └── terraform.md               # Minimalist IaC, Provider ~> 7.0, GCS remote backend
│
├── shell/                          # Terminal & Shell Environment
│   └── powershell/
│       └── profile.ps1             # PowerShell profile with Oh-My-Posh and productivity aliases
│
└── templates/                      # Clean Scaffolding Starters
    ├── .dockerignore               # Hermetic container build exclusions
    ├── .env.example                # Safe environment variable template with zero secrets
    ├── .gcloudignore               # Cloud Build upload filter
    └── terraform/                  # Starter Terraform module (backend, provider, core APIs)
        ├── backend.tf
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

---

## Key Highlights

### 1. AI & Agentic Engineering (`ai/`)
- **System Instructions (`ai/instructions/GEMINI.md`)**: Implements the Joi Cognitive Interface—pairing emotional design and psychological safety with strict typing, architectural review, and anti-pattern prevention for LLM assistants (Google Gemini, Antigravity, Claude, Cursor).
- **Reusable Skills (`ai/skills/`)**: Standalone, standardized agent skills adhering to the `SKILL.md` specification for ADR creation, PRD authoring, secure Git publishing, and automated testing.

### 2. Engineering Standards (`standards/`)
- **Python**: Enforces `uv` package management, `python == 3.13.5`, strict typing via **Mypy**, unified formatting via **Ruff**, and PEP 585/604 idioms.
- **Google Cloud**: Establishes global naming conventions (`af-*` prefix), Cloud Run stateless container standards, and Zero-Trust credential management.
- **Data & ML Engineering**: Documents BigQuery partitioning and clustering strategies, Storage Write API streaming patterns, and Vertex AI cognitive model hierarchy selection.
- **Terraform**: Outlines minimalist, modular IaC conventions targeting HashiCorp Google Provider `~> 7.0` and GCS remote state storage.

### 3. Shell Environment (`shell/`)
- **PowerShell (`shell/powershell/profile.ps1`)**: Configures [Oh-My-Posh](https://ohmyposh.dev/) prompt (`froczh` theme), sets UTF-8 console encoding, and provides rapid shortcuts for Git, directory navigation, and Python virtual environment activation.

---

## Usage & Integration

### Linking the PowerShell Profile (Windows)
To point your active PowerShell session to this profile:
```powershell
# In PowerShell:
$ProfileDir = Split-Path -Parent $PROFILE
if (!(Test-Path $ProfileDir)) { New-Item -ItemType Directory -Path $ProfileDir -Force }
Copy-Item ".\shell\powershell\profile.ps1" $PROFILE
```

### Scaffolding a New Project
When spinning up a new repository:
1. Copy `templates/.dockerignore` and `templates/.gcloudignore` to the project root.
2. Copy `templates/.env.example` to `.env` and fill in local secrets.
3. Link or reference `ai/instructions/GEMINI.md` as your project's assistant instructions.

---

## License

Licensed under the [Apache License, Version 2.0](LICENSE).
