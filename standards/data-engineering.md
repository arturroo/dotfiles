# Data Engineering Standards & Solutions (Anti)patterns

These standards define best practices for building robust, scalable, and cost-efficient data pipelines and analytical stores on Google Cloud.

---

## 1. BigQuery Architectural Patterns

### Partitioning & Clustering
- **Always Partition:** Tables with time-series or append-only events must be partitioned by ingestion time or event timestamp (`timestamp`).
- **Cluster by High-Cardinality Query Keys:** Cluster tables by frequently filtered fields (e.g. `session_id`, `user_id`, `actor`, `status`). Clustering reduces scanned bytes and improves query response times without storage overhead.
- **Cost & Quota Awareness:**
  - Avoid `SELECT *` in production queries and pipelines.
  - Always project only necessary columns.

### Querying BigQuery CLI (`bq`) via PowerShell
When running ad-hoc queries from Windows PowerShell, use standard SQL with single quotes to prevent backtick conflicts with PowerShell escape sequences:
```powershell
bq query --use_legacy_sql=false --project_id=my-project-id 'SELECT timestamp, session_id, actor, SUBSTR(content, 1, 60) AS preview FROM `my-project-id.my-dataset-id.my-table-id` ORDER BY timestamp DESC LIMIT 10'
```

---

## 2. Storage Tiering & Hybrid Stores (BigQuery vs. Firestore)

| Storage Layer | Primary Purpose | Latency Target | Query Pattern |
| :--- | :--- | :--- | :--- |
| **Firestore (`fs-`)** | Operational state, session cache, task graphs | Single-digit ms | Point lookups by Document ID, simple equality filters |
| **BigQuery (`bq-`)** | Analytical store, audit trails, event telemetry | Hundreds of ms to seconds | Aggregations, window functions, complex joins |
| **Cloud Storage (`gs://`)** | Raw artifact staging, large files, uncompressed inputs | Tens of ms | Blob read/write, prefix scans |

---

## 3. Pipeline Resilience & Idempotency

- **Idempotent Writes:**
  - Every pipeline step must produce identical results when executed multiple times with the same input.
  - Use deterministic record hashing (e.g. SHA-256 over canonical business keys) as dedup IDs.
- **Write-Audit-Publish Pattern:**
  - Stage raw ingestion data in isolated staging prefixes or tables.
  - Run deterministic validation gates before merging into serving datasets.
- **Granular Entity-Level Observability:**
  - Deterministic pipeline tools must log individual entity progress and status with explicit counters (e.g., `Processing item [1/50]: customer_id=123`).
  - When validation fails, log a `WARNING` with the exact violation rule, schema path, and reason.

---

## 4. Engineering (Anti)patterns to Avoid

* ❌ **Antipattern: Querying Unpartitioned Raw Tables:** Scanning full tables for point-in-time checks exhausts query budgets.
* ❌ **Antipattern: Hardcoded Connection Strings:** Never embed database URLs or tokens in pipeline code.
* ❌ **Antipattern: Binary/Base64 Dumps in Audit Tables:** Storing multi-megabyte payloads in operational logs or BigQuery tables bloats egress and costs. Always persist large artifacts to GCS and store strictly GCS URIs, MIME types, byte sizes, and checksums in BigQuery.
