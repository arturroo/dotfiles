# Security Code Review Report Template

Use this structure when generating `<task_dir>/code_review/security_review_YYYYMMDDHHmmss.md`. Always write the report in **English** and use **relative links** to repository files.

```markdown
# Security Code Review Report: <Feature / Branch Title>

**Date:** YYYY-MM-DD  
**Branch Reviewed:** `<branch-name>` (compared against `main`)  
**Reviewer:** Joi — Principal Application, Cloud, Data & AI Security Architect  
**Scope:** <Concise summary of architectural components, Cloud Functions, pipelines, models, and UI routes reviewed>  
**Overall Security Posture:** <🟢 **STRONG / APPROVED** | 🟡 **CONDITIONALLY APPROVED (Action Required on P0/P1)** | 🔴 **BLOCKED (Critical Vulnerabilities Found)**>

---

## 1. Executive Summary

<2–3 paragraphs summarizing the business/technical context of the changes, what security controls are already well-implemented, and the primary risk themes discovered during the audit.>

| ID | Severity | Category / CWE | Component / File | Finding Summary | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SEC-01** | 🔴 **HIGH (P0)** | `CWE-...` | `[file.py](relative/path/to/file.py)` | <Short summary> | Open |
| **SEC-02** | 🟠 **MEDIUM (P1)** | `CWE-...` | `[Component.js](relative/path/to/Component.js)` | <Short summary> | Open |

---

## 2. Detailed Vulnerability Analysis & Remediations

### [SEC-01] <Severity>: <Clear Vulnerability Title>
* **Category:** `<Domain>` / `<CWE-ID>: <CWE Name>`
* **Location:** [`path/to/file.py`](../../../../path/to/file.py#L10-L25)

#### Vulnerability Description
<Precise technical explanation of the root cause, the untrusted source, the missing validation/auth boundary, and the concrete exploit scenario.>

#### Remediation
<Actionable architectural fix + drop-in code snippet showing the secure implementation.>

---

## 3. Multi-Layered Input Validation & Defense-in-Depth Matrix

To enforce fail-fast gatekeeping (stopping execution and raising an actionable error immediately upon malformed or malicious input), apply the following validation rules across all modified entry points:

| Endpoint / Schema | Parameter | Type | Constraints (Length / Regex / Allowed Values) | Fail-Fast Security Rule |
| :--- | :--- | :--- | :--- | :--- |
| `<Endpoint/Model>` | `<field>` | `<type>` | `<max_length, pattern, Literal>` | Reject `<`, `>`, control chars (`\r\n\x00`), or invalid types with HTTP 400/422. |

---

## 4. Positive Security Observations (What Was Done Well)
* ✅ **<Control 1>:** <Explanation with relative file link>
* ✅ **<Control 2>:** <Explanation with relative file link>

---

## 5. Proposed Additions to Global / Project `GEMINI.md`
*(Include only when new systemic security standards emerged during the review)*

```markdown
- **<Rule Name>**: <Concise, enforceable rule text for GEMINI.md>
```
```
