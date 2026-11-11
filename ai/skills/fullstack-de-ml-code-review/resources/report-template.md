# Principal Fullstack, Data Engineering & ML Code Review Report Template

Use this structure when generating `<task_dir>/code_review/fullstack_review_YYYYMMDDHHmmss.md` (e.g. `fullstack_review_20261105173908.md`). Always write the report file in **English** and use **strictly relative repository links** (`../../../../path/to/file.py#L10-L20`) so no local machine paths leak to GitHub.

```markdown
# Code Review: <Story / Feature Title>

**Reviewer:** Joi (Principal Google Fullstack, Data Engineering & ML Systems Perspective)  
**Author / Decision-Maker:** Artur Fejklowicz  
**Branch:** `<branch-name>` (`<short-sha>`)  
**Target Branch:** `origin/main`  
**Date:** YYYY-MM-DD  
**Status:** <**Approved** | **Approved with Minor Comments** | **Needs Work (Blocked on Critical Findings)**>  

---

## 1. Executive Summary

<1–2 concise paragraphs summarizing the scope of the branch across Fullstack, Data Engineering, Cloud IaC, and ML/GenAI, highlighting the core business value delivered.>

### Strengths & Architectural Highlights
* **<Strength 1>:** <Concise explanation with relative link>
* **<Strength 2>:** <Concise explanation with relative link>
* **<Strength 3>:** <Concise explanation with relative link>

---

## 2. Findings by Severity

```
+---------------------------------------------------------------------------------------+
| SEVERITY BREAKDOWN                                                                    |
|  - Severity 1 (P0 Critical / Blockers: Security, Crash, IaC, Data Loss): X findings   |
|  - Severity 2 (P1 High / Logic, Contracts, Actionable Errors, ML/DE): Y findings      |
|  - Severity 3 (P2 Medium / Edge Cases, Packaging, Tech Debt): Z findings              |
+---------------------------------------------------------------------------------------+
```

---

### Severity 1: Critical Blockers (Must Fix Before Merge)

#### 1.1 [<Domain Tag>] <Clear Finding Title>
* **Files:**
  * [`path/to/file.py`](../../../../path/to/file.py#L10-L45)
* **Root Cause:**  
  <Precise technical explanation with relevant code excerpt.>
* **Impact:**  
  <Concrete production impact: runtime crash, data loss, silent contract mismatch, auth bypass, or IAM/Eventarc failure.>
* **Remediation:**  
  <Step-by-step fix with drop-in code snippet.>

---

### Severity 2: High Priority (Business Logic, Data Contracts & Policy Compliance)

#### 2.1 [<Domain Tag>] <Clear Finding Title>
* **Files:**
  * [`path/to/Component.js`](../../../../path/to/Component.js#L100-L130)
* **Root Cause:**  
  <Explanation>
* **Remediation:**  
  <Fix + code snippet>

---

### Severity 3: Medium Priority (Edge Cases, Observability & Maintainability)

#### 3.1 <Finding Title>
* **File:** [`path/to/file.py`](../../../../path/to/file.py#L50)
* **Issue:** <Brief explanation>
* **Fix:** <Concise remediation>

---

## 3. Recommended Additions to `GEMINI.md` (Global & Project Governance)
*(Include whenever the review uncovers reusable standards across Fullstack, GCP IaC, Data Engineering, or ML/GenAI)*

### 3.1 Proposals for Global `GEMINI.md` (`~/.gemini/GEMINI.md`)
> - **<Rule Title>**: <Precise, enforceable rule text in English.>

### 3.2 Proposals for Project `GEMINI.md`
> - **<Rule Title>**: <Precise, enforceable project rule text in English.>

---

## 4. Verification & Validation Checklist

- [ ] **<Check 1>:** <Concrete verification command or test scenario>
- [ ] **<Check 2>:** <Concrete verification command or test scenario>
```
