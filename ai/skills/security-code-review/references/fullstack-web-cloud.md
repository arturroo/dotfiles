# Fullstack Web, API & Cloud-Native Security Checklist (2026)

Read and apply this checklist when the diff touches Frontend (React / Next.js), Backend APIs (Cloud Functions / Cloud Run / FastAPI / Flask), Firebase (Hosting, Auth, Firestore, Storage), or Terraform IaC.

---

## 1. Authentication, Authorization & Reverse Proxy Boundaries

- **Firebase Hosting -> Cloud Run / Functions Gen 2 (`allUsers` Transport):**
  - Because Firebase Hosting rewrites do not synthesize IAM OIDC tokens, public `invoker_member = "allUsers"` endpoints rely 100% on application-layer authentication.
  - Verify every state-changing or privileged endpoint enforces **both** `X-Firebase-AppCheck` (`app_check.verify_token`) and `X-Firebase-Auth: Bearer <ID_TOKEN>` (`auth.verify_id_token` + `decoded.get("admin") is True`).
- **OIDC Token Verification (Eventarc / Cloud Scheduler / Internal Webhooks):**
  - Verify `verify_oauth2_token` checks the `aud` (Audience) claim against an explicit canonical URL/service list.
  - Verify the caller identity (`payload.get("email")`) is checked against an **exact project Service Account allowlist** (e.g., `415999574010-compute@developer.gserviceaccount.com` or `sa-...@project.iam.gserviceaccount.com`). Reject wildcard suffixes like `.endswith("-compute@developer.gserviceaccount.com")` which allow cross-tenant GCP project spoofing.
- **CORS Configuration:**
  - Verify backend CORS (`Access-Control-Allow-Origin`) and Cloud Storage CORS (`storage.cors.json`) whitelist only explicit production domains and authorized preview patterns—never `*` on authenticated endpoints or `localhost` in production manifests.

---

## 2. Injection, XSS & Client-Side Execution Isolation

- **Stored & Reflected HTML/XSS in Admin Panels & Emails:**
  - Check all fields interpolated into HTML email templates (`html_body`) or admin views: `name`, `email`, `subject`, `message`, `product_sku`, AI-generated summaries, and translated strings.
  - Ensure `html.escape(val, quote=True)` is applied to **every** variable, including inside `<title>...</title>` tags (an attacker can inject `</title><script>...` or `</title><img src=x onerror=...>`).
  - Never render HTML email bodies or rich external content via `dangerouslySetInnerHTML`. Enforce `<iframe sandbox="" srcDoc={html} referrerPolicy="no-referrer" />` (`sandbox=""` without `allow-scripts` or `allow-same-origin`).
- **JSON-LD & SSR Script Tag Breakout:**
  - Whenever `JSON.stringify(data)` is injected into `<script type="application/ld+json">`, verify `.replace(/</g, '\\u003c')` is applied so a payload containing `</script><script>` cannot break out of the script block during SSR.
- **URL Scheme & Open Redirect Validation:**
  - Any user- or CMS-supplied link rendered in `<a href={...}>` or `<img src={...}>` must be validated to allow only `https://` (or explicit internal `/` paths without `//` protocol-relative bypasses), blocking `javascript:`, `data:`, and `vbscript:` URIs.
  - Next.js `redirects` in `next.config.ts` and dynamic route redirects must validate destination paths to prevent Open Redirects (`CWE-601`).

---

## 3. Next.js / React Server Components (RSC) & Hydration Security

- **RSC Flight Payload Over-Posting / Data Leakage (`CWE-200`):**
  - Never pass raw Firestore documents or backend ORM entities (`{ id: doc.id, ...doc.data() }`) directly from a Server Component (`page.tsx`) as props into a `'use client'` component (`*Client.tsx`).
  - Next.js serializes all props passed to Client Components into inline `<script>self.__next_f.push(...)</script>` HTML payloads visible in page source.
  - Verify an explicit **DTO / Whitelist Mapper** (`mapToPublicDto`) strips internal drafts (`ai_suggestions`, internal notes, supplier prices, author UIDs, unpublished timestamps) on the server before crossing the RSC boundary.
- **Cache Poisoning & ISR Revalidation (`/api/revalidate`):**
  - Ensure on-demand ISR revalidation endpoints require cryptographic authentication (OIDC or HMAC secret) and validate the `path` parameter (must start with `/`, max length <= 256, no external URLs).

---

## 4. Firestore & Cloud Storage Security Rules Architecture

- **Document-Level Rule Granularity (`CWE-200`):**
  - Firestore Security Rules cannot filter individual fields within a document (`allow read: if true;` exposes the **entire** document).
  - Never store internal admin drafts, AI strategy notes, or PII inside publicly readable documents (e.g., `page_contents/home` or `products/{id}`).
  - Segregate internal data into a dedicated admin-only collection (`studio_internal/...`) or protected subcollection (`.../private_meta/ai_drafts`) within the **same database** (`florkadb`) to preserve atomic `WriteBatch` transactions while enforcing `allow read, write: if isAdmin();`.
- **Storage Master Asset Protection:**
  - Verify public read rules match only derived web variants (`.*_(card|thumb|full)\\.webp$`), keeping master originals (`raw.jpg`) strictly restricted to `isAdmin()`.

---

## 5. File Uploads, Attachments & Rich Content Security

- **Direct-to-Storage Signed URLs vs. Inline Base64:**
  - Flag any design that sends binary files or base64 `data:image/...` strings inside JSON payloads or Firestore documents (1 MiB document limit, wallet/memory exhaustion).
  - Attachments must upload via signed URLs / Firebase Storage with strict size caps, double-checked MIME validation (Content-Type + Magic Bytes inspection for `%PDF-`, `\x89PNG`, `\xFF\xD8\xFF`), `Content-Disposition: attachment` on download, and zero SVG/HTML execution in the browser.
