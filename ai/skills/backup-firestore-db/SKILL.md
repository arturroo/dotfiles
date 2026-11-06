---
name: backup-firestore-db
description: >-
  Export a Cloud Firestore database (e.g. florkadb) to Google Cloud Storage (GCS)
  with a timestamped snapshot path (-yyyyMMddHHmmss).
author: Artur Fejklowicz
copyright: "Copyright (c) 2026 Artur Fejklowicz"
license: Apache-2.0
version: 1.0.0
updated_at: 2026-11-06
---

# Firestore Database Backup Skill

This skill provides step-by-step PowerShell procedures to export a Cloud Firestore database to Google Cloud Storage (GCS) with timestamped snapshot directories.

## Prerequisites
- Operating System: Windows 11 (PowerShell)
- Active GCP Project: `floralkaleidoskop` (`gcloud config set project floralkaleidoskop`)
- Target Backup Bucket: `gs://floralkaleidoskop-backups/fs/`
- Primary Database: `florkadb`

---

## 1. Export Firestore Database to GCS

To take an immediate snapshot backup with a timestamp formatted with `-yyyyMMdd-HHmmss`:

```powershell
# 1. Target database & timestamp
$database = "florkadb"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$exportUri = "gs://floralkaleidoskop-backups/fs/$database/$database-$timestamp"

# 2. Trigger asynchronous Firestore export
gcloud firestore export $exportUri --database=$database
```

To export only specific collections (e.g., `products` and `product_categories`):
```powershell
gcloud firestore export $exportUri --database=$database --collection-ids=products,product_categories
```

---

## 2. Verify Snapshot Artifacts in Cloud Storage

After export completes, verify that metadata and data partitions exist in GCS:

```powershell
gcloud storage ls --recursive $exportUri/
```

### Expected Output Structure:
```
$exportUri/
  ├── <database>-<timestamp>.overall_export_metadata
  └── all_namespaces/
      └── all_kinds/
          ├── all_namespaces_all_kinds.export_metadata
          ├── output-0
          └── output-1 ...
```

---

## 3. List Past Backups

To inspect all existing backups for a database:
```powershell
gcloud storage ls gs://floralkaleidoskop-backups/fs/florkadb/
```
