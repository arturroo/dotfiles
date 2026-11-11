# Data Engineering, Machine Learning & GenAI Systems Review Checklist (2026)

Read and apply this checklist when the diff touches Data Engineering pipelines (BigQuery, Firestore batch/streaming, Eventarc, Pub/Sub, GCS, Dataform/dbt, ETL/ELT jobs) or Machine Learning / GenAI systems (Vertex AI, Gemini 3.5+/3.8, Grounding, RAG, Pydantic schemas, feature engineering, MLOps).

---

## 1. Data Engineering & Analytical Pipelines (BigQuery, Firestore, Event-Driven ETL)

- **BigQuery Architecture, Cost & Performance Optimization:**
  - **Partitioning & Clustering:** Verify new or modified BigQuery tables define appropriate time-unit/ingestion partitioning (`DATE(created_at)`, `_PARTITIONTIME`) and clustering columns (up to 4 high-cardinality filter/join keys) aligned with query access patterns.
  - **Query Cost Guards & Pruning:** Flag `SELECT *` on columnar tables, missing partition filters in `WHERE` clauses, and automated jobs lacking `maximum_bytes_billed` in `QueryJobConfig`.
  - **Parameterized Queries:** Ensure all dynamic values in SQL use `ScalarQueryParameter` / `ArrayQueryParameter`—never Python f-strings or `.format()`.
- **Pipeline Idempotency, Watermarks & Exactly-Once Semantics:**
  - **Eventarc / Pub/Sub Replay Safety:** Because cloud event buses guarantee *at-least-once* delivery, verify every consumer is idempotent. Check that retries or duplicate deliveries do not send duplicate transactional emails, create duplicate rows (`INSERT` without `MERGE` / deduplication key), or double-increment counters.
  - **Batch & Streaming Write Semantics:**
    - In BigQuery: Verify load/query jobs explicitly specify `write_disposition` (`WRITE_TRUNCATE` for partition overwrites, or deterministic `MERGE` statements) rather than blind `WRITE_APPEND` that duplicates data on retry.
    - In Firestore: Verify multi-document updates (e.g., updating a live document AND archiving its previous version to `versions/{v}`) execute atomically via `db.batch()` or `@firestore.transactional` so partial failures cannot corrupt version history.
- **Schema Evolution, Data Contracts & Timezone Hygiene:**
  - Verify backward/forward compatibility when adding or renaming fields in BigQuery tables, Firestore collections, or Pydantic models (`Optional` with safe defaults or explicit migration scripts).
  - Enforce UTC everywhere (`datetime.now(timezone.utc)`, BigQuery `TIMESTAMP`) and explicit timezone conversion (`ZoneInfo("Europe/Zurich")`) only at presentation/reporting boundaries.

---

## 2. Machine Learning & GenAI Engineering (Vertex AI, Gemini 3.5+/3.8, MLOps)

- **Gemini 3.5+ / 3.8 Model & Thinking Configuration Standard:**
  - **Strict Model Whitelist:** Only Gemini 3.5+ and next-gen models are permitted (`gemini-3.5-flash-lite`, `gemini-3.8-flash`, Argon, Carbon). Flag any reference to `gemini-1.5-*`, `gemini-2.0-*`, or `gemini-2.5-*` as a critical policy violation.
  - **Thinking Level Enforcement:** Reasoning MUST be configured strictly via `thinking_level` (`"LOW"`, `"MEDIUM"`, `"HIGH"`) inside `types.ThinkingConfig(thinking_level=...)`. Flag any use of legacy `thinking_budget`.
  - **Sampling Parameter Compatibility:** Verify `top_p` is omitted when `ThinkingConfig` is enabled to prevent SDK/API parameter conflicts.
- **Prompt Architecture & Materialization Pattern:**
  - **Single-Read Materialization (`resolved_content`):** Verify runtime Cloud Functions fetch materialized prompts in a single read from `ai_prompts/{task_id}` (`resolved_content`) rather than performing N+1 fan-out reads across modular `ai_components` at inference time.
  - **Task ID Existence Verification:** Whenever frontend or backend code constructs a dynamic prompt `task_id` (e.g., `f"translate_{object}_{field}"`), verify that the exact `task_id` is defined and seeded in `scripts/seed-ai-prompts.py`.
- **Structured Outputs, Grounding & Hallucination Guardrails:**
  - **Pydantic Schema Discipline:** Verify LLM calls returning structured data pass `response_mime_type="application/json"` and `response_schema=<PydanticModel>` with clear `Field(description=...)` instructions.
  - **Google Search Grounding (`types.GoogleSearch()`):** When grounding is enabled (`enable_google_search=True`), verify that grounding metadata (`web_search_queries`, source URIs) is safely extracted with null-safe fallbacks (`getattr(..., None) or []`) since Gemini may not trigger search on every turn.
  - **Untrusted Input Delimiters:** Ensure user-supplied text or external search snippets interpolated into prompts are wrapped in clear XML tags and cannot override system instructions or output formatting rules.
- **Classical ML & Feature Engineering Best Practices (When Applicable):**
  - **Data Leakage & Train-Serve Skew:** Check for target leakage (using future/post-event features in training splits), improper random splitting on time-series data (require temporal out-of-time splits), and preprocessing skew (fitting scalers/encoders on the full dataset instead of `train` only).
  - **Reproducibility & Lineage:** Verify random seeds, dataset snapshot versions/timestamps, hyperparameters, and evaluation metrics (ROC-AUC, PR-AUC, RMSE, calibration) are logged deterministically.
