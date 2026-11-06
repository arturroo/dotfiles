---
name: restore-firestore-db
description: >-
  Restore a Cloud Firestore database from a Google Cloud Storage (GCS) export snapshot
  into a target database, recreate composite indexes, and verify collection and document parity.
author: Artur Fejklowicz
copyright: "Copyright (c) 2026 Artur Fejklowicz"
license: Apache-2.0
version: 1.0.0
updated_at: 2026-11-06
---

# Firestore Database Restore Skill

This skill provides step-by-step PowerShell procedures to restore a Cloud Firestore database from a Google Cloud Storage (GCS) snapshot into a new or existing target database, recreate required composite indexes, and verify data parity.

## Prerequisites
- Operating System: Windows 11 (PowerShell)
- Active GCP Project: `floralkaleidoskop` (`gcloud config set project floralkaleidoskop`)
- Target Location: `europe-west6` (Zürich)
- GCS Backup Bucket: `gs://floralkaleidoskop-backups/fs/`

> [!IMPORTANT]
> **Database ID Naming Constraint:**
> Cloud Firestore database IDs must be between 4 and 63 characters and match the regex `/[a-z][0-9]-/`. Underscores (`_`) are strictly prohibited and rejected with `INVALID_ARGUMENT`. Always use hyphens (e.g. `florkadb-restore-backup`, never `florkadb_restore_backup`).

---

## 1. Create Target Database in Zürich

If restoring into a new database instance:

```powershell
$targetDb = "florkadb-restore-backup"
gcloud firestore databases create `
  --database=$targetDb `
  --location=europe-west6 `
  --type=firestore-native
```

---

## 2. Import Snapshot from Cloud Storage

Pass the GCS export directory URI (e.g. `gs://floralkaleidoskop-backups/fs/florkadb/<timestamp>`):

> [!NOTE]
> Provide the folder path, not the `.overall_export_metadata` file path. `gcloud firestore import` automatically appends `<folder>.overall_export_metadata`.

```powershell
$exportUri = "gs://floralkaleidoskop-backups/fs/florkadb/<folder-name>"
gcloud firestore import $exportUri --database=$targetDb
```

---

## 3. Verify Collection & Document Parity

Run the automated parity verification script comparing source and target databases:

```powershell
uv run python scripts/verify-firestore-parity.py --source florkadb --target $targetDb
```

This verifies that:
1. Every collection present in source exists in target.
2. Every collection has identical document counts.
3. Exits with code `0` on 100% parity; exits with code `1` with an actionable diagnosis on discrepancy.

---

## 4. Recreate Composite Indexes (Production Restore Only)

Composite indexes are not restored automatically by `gcloud firestore import`. When restoring a permanent database for production use, provision the required indexes:

```powershell
# Index 1: products (status ASC, position DESC)
gcloud firestore indexes composite create `
  --database=$targetDb `
  --collection-group=products `
  --field-config="field-path=status,order=ascending" `
  --field-config="field-path=position,order=descending"

# Index 2: products (category_ids CONTAINS, status ASC, position DESC)
gcloud firestore indexes composite create `
  --database=$targetDb `
  --collection-group=products `
  --field-config="field-path=category_ids,array-config=contains" `
  --field-config="field-path=status,order=ascending" `
  --field-config="field-path=position,order=descending"

# Index 3: products (status ASC, position ASC)
gcloud firestore indexes composite create `
  --database=$targetDb `
  --collection-group=products `
  --field-config="field-path=status,order=ascending" `
  --field-config="field-path=position,order=ascending"

# Index 4: products (category_ids CONTAINS, status ASC, position ASC)
gcloud firestore indexes composite create `
  --database=$targetDb `
  --collection-group=products `
  --field-config="field-path=category_ids,array-config=contains" `
  --field-config="field-path=status,order=ascending" `
  --field-config="field-path=position,order=ascending"

# Index 5: product_categories (status ASC, position ASC)
gcloud firestore indexes composite create `
  --database=$targetDb `
  --collection-group=product_categories `
  --field-config="field-path=status,order=ascending" `
  --field-config="field-path=position,order=ascending"
```

Verify status until all indexes show `READY`:
```powershell
gcloud firestore indexes composite list --database=$targetDb
```

---

## 5. Teardown / Deletion (For Temporary Restores)

If the database was restored for testing or verification purposes, delete it once verified:

```powershell
gcloud firestore databases delete --database=$targetDb --quiet
```
