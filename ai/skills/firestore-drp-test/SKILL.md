---
name: firestore-drp-test
description: >-
  Execute an automated end-to-end Firestore Disaster Recovery Plan (DRP) drill:
  back up florkadb to GCS with a timestamped snapshot (-yyyyMMddHHmmss), restore into
  florkadb-restore-backup, verify 100% data and collection parity, and safely delete the temporary database.
author: Artur Fejklowicz
copyright: "Copyright (c) 2026 Artur Fejklowicz"
license: Apache-2.0
version: 1.0.0
updated_at: 2026-11-06
---

# Firestore DRP End-to-End Test Skill

This skill orchestrates a complete Disaster Recovery Plan (DRP) verification drill by composing the `backup-firestore-db` and `restore-firestore-db` skills. It guarantees that our backup and restore pipelines are 100% operational, validates data integrity, and cleans up all temporary resources.

## Prerequisites
- Operating System: Windows 11 (PowerShell)
- Active GCP Project: `floralkaleidoskop` (`gcloud config set project floralkaleidoskop`)
- Target Location: `europe-west6` (Zürich)
- GCS Backup Bucket: `gs://floralkaleidoskop-backups/fs/`
- Production Database: `florkadb`
- Temporary Drill Database: `florkadb-restore-backup` (Note: database IDs cannot contain underscores)

---

## 1. End-to-End DRP Drill Workflow

Run the following 4-stage PowerShell workflow to validate disaster recovery:

### Stage 1: Export Snapshot to GCS (`backup-firestore-db`)
```powershell
$sourceDb = "florkadb"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$exportUri = "gs://floralkaleidoskop-backups/fs/$sourceDb/$sourceDb-$timestamp"

Write-Host "Stage 1: Exporting $sourceDb to $exportUri..." -ForegroundColor Cyan
gcloud firestore export $exportUri --database=$sourceDb
```

### Stage 2: Restore Snapshot into Temporary Database (`restore-firestore-db`)
```powershell
$testDb = "florkadb-restore-backup"

Write-Host "Stage 2: Creating native Firestore test database $testDb in europe-west6..." -ForegroundColor Cyan
gcloud firestore databases create `
  --database=$testDb `
  --location=europe-west6 `
  --type=firestore-native

Write-Host "Stage 2b: Importing snapshot into $testDb..." -ForegroundColor Cyan
gcloud firestore import $exportUri --database=$testDb
```

### Stage 3: Automated Parity & Data Integrity Verification
```powershell
Write-Host "Stage 3: Running automated parity verification..." -ForegroundColor Cyan
uv run python scripts/verify-firestore-parity.py --source $sourceDb --target $testDb

if ($LASTEXITCODE -ne 0) {
    Write-Error "DRP Verification FAILED! Parity mismatch detected between $sourceDb and $testDb."
    exit 1
}
Write-Host "Parity verification PASSED with 100% collection and document match!" -ForegroundColor Green
```

### Stage 4: Teardown & Deletion
```powershell
Write-Host "Stage 4: Deleting temporary test database $testDb..." -ForegroundColor Yellow
gcloud firestore databases delete --database=$testDb --quiet

Write-Host "Stage 4b: Confirming active databases list..." -ForegroundColor Cyan
gcloud firestore databases list
```

---

## 2. Success Criteria
A successful DRP test run must satisfy:
1. `gcloud firestore export` exits with code 0 and populates GCS partitions.
2. `gcloud firestore databases create` successfully provisions `$testDb` in `europe-west6`.
3. `gcloud firestore import` restores all namespaces and collections without error.
4. `uv run python scripts/verify-firestore-parity.py` reports `0` mismatches across all collections (`ai_components`, `ai_prompts`, `contact_messages`, `email_logs`, `messages`, `page_contents`, `product_categories`, `product_types`, `products`, `site_settings`, `trend_reports`).
5. `gcloud firestore databases delete` successfully purges `$testDb`, leaving only production databases (`florkadb`, `studiodb`, `wwwdb`).
