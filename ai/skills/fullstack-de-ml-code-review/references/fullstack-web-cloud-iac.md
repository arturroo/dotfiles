# Fullstack Web, API & Cloud-Native IaC Review Checklist (2026)

Read and apply this checklist when the diff touches Frontend (React / Next.js), Backend APIs (Cloud Functions Gen 2 / Cloud Run / FastAPI / Flask), Firebase (Hosting, Auth, Firestore, Storage), or Terraform IaC.

---

## 1. Frontend Architecture, State Management & End-to-End Contracts (React / Next.js)

- **State Integrity & Partial Update Hazards:**
  - When loading partial payloads (e.g., AI-generated seasonal drafts, patch updates, or filter presets) into form state (`setFormContent`), verify the code **merges** keys (`prev => ({ ...prev, ...draft })`) rather than overwriting the entire document object and destroying unedited fields (such as `faq_items`, `trust_pillars`, or metadata).
  - Verify all tabs, route segments, and conditional views declared in navigation have corresponding rendered bodies and empty-state handlers.
- **Next.js App Router, SSG/ISR & Cache Invalidation:**
  - Verify `generateStaticParams()` routes configure `export const dynamicParams = true` when on-demand ISR (`revalidatePath`) creates or updates entities post-build, calling `notFound()` explicitly for missing entities.
  - Verify server-to-client component boundaries pass clean, serializable DTOs and never pass raw Firestore `Timestamp` objects or unserialized classes into `'use client'` components or `JSON-LD` scripts.
- **SEO, Structured Data (`JSON-LD`) & Localization:**
  - Check canonical URLs, `hreflang` alternates (`de-CH`, `pl`, `x-default`), single `<h1>` hierarchy per page, and Schema.org `JSON-LD` validity.
  - Verify outbound customer communication workflows (e.g., admin email replies) target only standard written languages (`de` Schweizer Hochdeutsch with `ss`, `pl`, `en`, `fr`, `it`) and never inject dialect (`ch` / Mundart) into formal outbound correspondence.
- **Mobile UX & Chromium/Adreno GPU Compositor Standards:**
  -Entity CRUD in admin apps must use dedicated full-page routes (`/new`, `/edit/:id`) rather than modals, and master-detail views (`MessagesPage`) must collapse cleanly on mobile (`<= 768px`).
  - Flag `backdrop-filter: blur(...)` underneath modals, giant `box-shadow: 0 0 0 9999em` spreads, or raw high-MP image decoding directly inside interactive DOM croppers.
  - Ensure rich HTML previews (such as email logs) render inside `<iframe sandbox="" srcDoc={...} />` rather than raw `dangerouslySetInnerHTML`.

---

## 2. Backend Microservices & Zero-Trust Reverse Proxy (Cloud Functions Gen 2 / Cloud Run)

- **Entry Point & Packaging Standards:**
  - Cloud Functions entry point function must be `main` (`def main(req):` or `def main(cloud_event):`).
  - Every Cloud Function must be **Gen 2 (`GEN_2`)** and define dependencies **exclusively in `pyproject.toml`** with exact `==` versions. Flag any `requirements.txt` file for removal/migration.
  - Verify all Pydantic validator dependencies (such as `email-validator` when `EmailStr` is imported) are present in `pyproject.toml`.
- **Dual-Caller Authentication on `allUsers` Endpoints:**
  - Services fronted by Firebase Hosting rewrites use `invoker_member = "allUsers"` and must enforce cryptographic authentication in application code:
    - **UI / Admin Callers:** Verify both `X-Firebase-AppCheck` (`firebase_admin.app_check.verify_token`) and `X-Firebase-Auth: Bearer <ID_TOKEN>` (`firebase_admin.auth.verify_id_token` + `decoded.get("admin") is True`).
    - **Cloud Scheduler / OIDC Callers:** Verify `Authorization: Bearer <OIDC_TOKEN>` via `google.oauth2.id_token.verify_oauth2_token(token, requests.Request())`, checking `email_verified is True` and matching `email` against an explicit service account allowlist. Never trust `User-Agent`, `X-CloudScheduler`, or exception string matching (`"iss" in str(e)`).
- **Python Runtime & Control-Flow Correctness:**
  - Check all conditional branches (e.g., CloudEvent `subject` parsing) to ensure local variables (`collection_name`, `doc_id`) are initialized before use in logging or downstream payloads (`UnboundLocalError` prevention).
  - Flag deprecated naive `datetime.utcnow()` calls; enforce timezone-aware `datetime.now(timezone.utc)`.

---

## 3. Infrastructure as Code (Terraform) & Firebase Configuration

- **Archive Packaging Exclusions:**
  - Every `archive_file` data source in Terraform must include the standard exclusion list:
    `excludes = [".git", ".venv", "__pycache__", ".pytest_cache", ".zips", "zips", ".gemini", "node_modules", ".DS_Store"]`
- **Service Account IAM Parity (`project_bindings`):**
  - Cross-check every SDK client initialized in Python against the function's Service Account IAM roles in `terraform/variables.tf`:
    - Vertex AI / `google-genai` (`vertexai=True`) -> requires `roles/aiplatform.user`
    - Firestore (`google-cloud-firestore`) -> requires `roles/datastore.user`
    - BigQuery (`google-cloud-bigquery`) -> requires `roles/bigquery.jobUser` + dataset-level `roles/bigquery.dataViewer` / `dataEditor`
    - Cloud Storage (`google-cloud-storage`) -> requires bucket-scoped `roles/storage.objectViewer` / `objectAdmin`
- **Eventarc & Hosting Rewrite Alignment:**
  - Verify every `firebase.json` rewrite rule (`source` -> `function`) matches a deployed HTTP Cloud Function name.
  - Verify every Eventarc `event_trigger` `document` filter in `terraform/variables.tf` matches all Firestore collections that the function's code expects to handle. Remember that a single Firestore Eventarc trigger supports only one `document` path pattern per trigger.
