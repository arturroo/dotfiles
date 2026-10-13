---
name: git-add-commit-and-push
description: >-
  Perform a secure Git publish workflow (audit, stage, conventional commit, push, and PR link). Use when the user asks to commit, stage, push, or publish changes to Git.
author: Artur Fejklowicz
updated_at: 2026-10-12
---

# Git Add, Commit and Push (Generic Git Workflow)

## Overview
This skill executes a secure, production-grade Git publishing workflow. It acts as an automated safety gate to prevent secret leakage, repository bloat, and blind staging, ensuring clean Conventional Commits and seamless Pull Request creation.

## Workflow

```mermaid
flowchart TD
    A["Trigger: git-add-commit-and-push"] --> B["Step 1: Security & Sensitive Data Leak Audit"]
    B -->|Secret / Key Detected!| B_HALT["HALT: Report leak & abort"]
    B -->|Safe| C["Step 2: Precise File-by-File Staging"]
    C --> D["Step 3: Strictly Technical Conventional Commit"]
    D --> E["Step 4: Remote Push & PR Generation"]
```

---

### Step 1: Security & Sensitive Data Leak Audit
Before staging any file, inspect all uncommitted and untracked changes (`git diff`, `git status --porcelain`).
Scan modified content against sensitive data patterns:
1. **API Keys, Secrets & Private Cryptographic Keys:**
   - Secret key variable names with actual values (e.g. `*_API_KEY = "..."`, `*_SECRET`, `*_TOKEN`).
   - Bearer authentication tokens, private SSH/RSA/EC keys (`-----BEGIN PRIVATE KEY-----`, `-----BEGIN RSA PRIVATE KEY-----`).
   - Service Account JSON keys (`"private_key": "-----BEGIN`).
2. **Hardcoded Resources & Environment Compliance:**
   - Database passwords, connection strings, or URIs containing embedded credentials (e.g. `postgres://user:pass@...`, `mongodb+srv://...`).
   - Hardcoded internal cloud resource URIs (e.g. private Cloud Storage buckets `gs://...`, `s3://...`) or private service endpoints in application code instead of referencing environment variables (`.env`).
   - Webhook URLs containing embedded secret tokens (e.g. Discord, Slack, Telegram webhook links).
   *(Note: Public documentation links, schema references such as `https://schema.org`, and verified public static assets are permitted).*
3. **Environment & Local Configuration Files:**
   - Accidental modification or tracking of local configuration files containing plain secrets (`.env`, `.env.local`, `.env.*.local`, `credentials.json`).

> [!CAUTION]
> **Zero-Leak Policy:** If ANY sensitive key, credential, hardcoded secret, or private resource URI is detected, **HALT IMMEDIATELY**. Report the exact file path and line reference to the user. DO NOT stage or commit.

---

### Step 2: Precise File-by-File Staging
Inspect the workspace using `git status --porcelain`.
Stage strictly relevant files for the current task/session file-by-file or by exact directory path.

#### Strict Staging Rules:
- **NEVER use catch-all staging:** Blind commands such as `git add .` or `git add -A` are strictly prohibited.
- **Mandatory Exclusions (Never Stage):**
  - **Binary assets:** Images (`*.png`, `*.jpg`, `*.jpeg`, `*.gif`, `*.ico`, `*.webp`), archives (`*.zip`, `*.tar`, `*.gz`), executables (`*.exe`, `*.dll`), and documents (`*.pdf`), unless explicitly requested as project assets.
  - **Environment & local secret files:** `.env`, `.env.local`, `.env.*.local`, credentials files.
  - **Scratch & temporary files:** Debug scripts, local dumps, uncommitted test caches, runtime logs (`*.log`), or scratch folders (e.g. `scratch/`, `.gemini/`).
- **Verify Staging:** Run `git diff --cached --name-status` to verify that only intended files are in the index.

---

### Step 3: Strictly Technical Conventional Commit
Formulate a commit message strictly adhering to the **Conventional Commits** specification:
`<type>(<scope>): <subject>`

* **Definition:**
  * **`<type>`:** Defines the structural intent of the change (what kind of change was introduced).
  * **`<scope>`:** Defines the specific module, feature, or architectural component affected by the change (what part of the system was modified).
  * **`<subject>`:** A concise, imperative summary of the change in lowercase (e.g. "add google oauth login", not "added google oauth login").

1. **Allowed Types:**
   * `feat` – New functional feature for the user or system
   * `fix` – Bug fix in code
   * `hotfix` – Urgent production bug fix or patch
   * `refactor` – Code change that neither fixes a bug nor adds a feature
   * `chore` – Maintenance tasks, build tooling, dependency updates
   * `docs` – Documentation only changes
   * `test` – Adding missing tests or correcting existing tests
   * `ci` – Changes to CI/CD workflows and deployment configurations
   * `perf` – Code change that improves performance
   * `build` – Changes that affect the build system or external dependencies

2. **Scope Derivation & Few-Shot Examples:**
   Derive `<scope>` automatically from the active Git branch name or primary directory modified:
   * Branch `feature/auth-oauth` ➔ `scope = auth`
     * Example: `feat(auth): integrate google oauth login`
   * Branch `feature/epic-12/seo/static-site-generation` ➔ `scope = seo`
     * Example: `feat(seo): configure generateStaticParams for static site generation`
   * Branch `hotfix/cart-calculation` ➔ `scope = cart`
     * Example: `hotfix(cart): fix vat calculation error for swiss addresses`
   * Branch `fix/checkout-discount` ➔ `scope = checkout`
     * Example: `fix(checkout): validate promo code expiration before payment intent`
   * Branch `infra/terraform-storage` ➔ `scope = infra`
     * Example: `chore(infra): provision cloud storage buckets and access policies`
   * Branch `docs/api-contracts` ➔ `scope = api`
     * Example: `docs(api): update openapi schema definitions for orders endpoint`

3. **Technical Summary & Bullets:**
   - Describe the architectural, functional, and structural changes.
   - Example structure:
     ```text
     feat(auth): implement session validation and custom claims

     - Add token verification middleware for admin routes
     - Cache public keys in local memory with 1h TTL
     - Update user schema definitions and unit tests
     ```

#### Quality Guidelines:
- **100% Technical Focus:** Focus exclusively on architecture, services, endpoints, data contracts, algorithms, configuration, and infrastructure.
- **ZERO Editorial Filler:** No conversational prose, storytelling, subjective commentary, or puzzles/lore.
- **ZERO Secrets:** NEVER include raw API keys, passwords, or tokens in commit messages.

---

### Step 4: Remote Push & PR Generation
1. Determine current active branch: `git branch --show-current`.
2. Push branch with upstream tracking:
   ```powershell
   git push -u origin <current-branch>
   ```
3. Extract remote repository URL (`git remote get-url origin` or `git remote -v`).
4. Generate and display the direct Pull Request / Merge Request URL:
   - **GitHub:** `https://github.com/<owner>/<repo>/pull/new/<current-branch>`
   - **GitLab:** `https://gitlab.com/<owner>/<repo>/-/merge_requests/new?merge_request%5Bsource_branch%5D=<current-branch>`
5. Present a clear, friendly summary to the user with the commit hash, staged file list, and clickable PR link.
