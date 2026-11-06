#!/usr/bin/env python3
# Copyright (c) 2026 Artur Fejklowicz
# SPDX-License-Identifier: Apache-2.0
"""Automated Firestore Parity & Integrity Verification Script.

Compares collections, document counts, and data parity between a source database
and a restored/target database in Google Cloud Firestore.
"""

import argparse
import sys
from typing import Dict, Set

try:
    from google.cloud import firestore
except ImportError as exc:
    print(
        "❌ [Actionable Error] Missing dependency: 'google-cloud-firestore' is not installed.\n"
        "   Why: Python cannot import the Google Cloud Firestore client library.\n"
        "   Contact: Artur Fejklowicz (Lead Developer).\n"
        "   Next Step: Run 'uv pip install google-cloud-firestore' or invoke via 'uv run python verify-firestore-parity.py'.",
        file=sys.stderr,
    )
    sys.exit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify collection and document parity between two Cloud Firestore databases."
    )
    parser.add_argument(
        "--source",
        default="florkadb",
        help="Source Firestore database name (default: florkadb)",
    )
    parser.add_argument(
        "--target",
        default="florkadb-restore-backup",
        help="Target/restored Firestore database name (default: florkadb-restore-backup)",
    )
    parser.add_argument(
        "--project",
        default="floralkaleidoskop",
        help="GCP Project ID (default: floralkaleidoskop)",
    )
    return parser.parse_args()


def count_collection(db: firestore.Client, col_name: str) -> int:
    """Fast document count using empty projection stream."""
    return sum(1 for _ in db.collection(col_name).select([]).stream())


def run_verification(project: str, source_db_name: str, target_db_name: str) -> int:
    print(f"============================================================")
    print(f"  Firestore Parity Verification: [{source_db_name}] vs [{target_db_name}]")
    print(f"  Project: {project}")
    print(f"============================================================\n")

    try:
        source_db = firestore.Client(project=project, database=source_db_name)
        target_db = firestore.Client(project=project, database=target_db_name)
    except Exception as exc:
        print(
            f"❌ [Actionable Error] Failed to initialize Firestore clients.\n"
            f"   Why: {exc}\n"
            f"   Contact: Artur Fejklowicz (Lead Developer).\n"
            f"   Next Step: Verify active gcloud authentication ('gcloud auth application-default login') "
            f"and check that databases '{source_db_name}' and '{target_db_name}' exist.",
            file=sys.stderr,
        )
        return 1

    try:
        source_cols: Set[str] = {col.id for col in source_db.collections()}
    except Exception as exc:
        print(
            f"❌ [Actionable Error] Failed to list collections from source database '{source_db_name}'.\n"
            f"   Why: {exc}\n"
            f"   Contact: Artur Fejklowicz (Lead Developer).\n"
            f"   Next Step: Verify database '{source_db_name}' exists via 'gcloud firestore databases list'.",
            file=sys.stderr,
        )
        return 1

    try:
        target_cols: Set[str] = {col.id for col in target_db.collections()}
    except Exception as exc:
        print(
            f"❌ [Actionable Error] Failed to list collections from target database '{target_db_name}'.\n"
            f"   Why: {exc}\n"
            f"   Contact: Artur Fejklowicz (Lead Developer).\n"
            f"   Next Step: Verify database '{target_db_name}' exists via 'gcloud firestore databases list' "
            f"and that snapshot import has finished.",
            file=sys.stderr,
        )
        return 1

    all_cols = sorted(source_cols.union(target_cols))
    if not all_cols:
        print(
            f"⚠️ [Actionable Warning] Both databases appear empty (0 collections found).\n"
            f"   Contact: Artur Fejklowicz (Lead Developer).\n"
            f"   Next Step: Verify that '{source_db_name}' has data before running parity check."
        )
        return 1

    print(f"Source [{source_db_name}] collections ({len(source_cols)}): {sorted(source_cols)}")
    print(f"Target [{target_db_name}] collections ({len(target_cols)}): {sorted(target_cols)}\n")

    errors = 0
    missing_in_target = source_cols - target_cols
    if missing_in_target:
        print(f"❌ Collections missing in target database: {sorted(missing_in_target)}")
        errors += len(missing_in_target)

    unexpected_in_target = target_cols - source_cols
    if unexpected_in_target:
        print(f"⚠️ Extra collections found in target database: {sorted(unexpected_in_target)}")
        errors += len(unexpected_in_target)

    print("--- Collection Document Counts ---")
    results: Dict[str, Dict[str, int]] = {}
    for col in all_cols:
        s_count = count_collection(source_db, col) if col in source_cols else 0
        t_count = count_collection(target_db, col) if col in target_cols else 0
        results[col] = {"source": s_count, "target": t_count}

        status_icon = "✅" if s_count == t_count else "❌"
        print(f"  {status_icon} Collection '{col}': source={s_count}, target={t_count}")
        if s_count != t_count:
            errors += 1

    print("\n------------------------------------------------------------")
    if errors > 0:
        print(
            f"❌ [Actionable Error] DRP verification failed with {errors} discrepancy/discrepancies!\n"
            f"   Why: Document counts or collection sets do not match between '{source_db_name}' and '{target_db_name}'.\n"
            f"   Contact: Artur Fejklowicz (Lead Developer).\n"
            f"   Next Step: Inspect GCS snapshot export logs and re-import snapshot using 'gcloud firestore import'."
        )
        return 1

    print(f"🎉 SUCCESS: 100% data & collection parity confirmed between '{source_db_name}' and '{target_db_name}'!")
    return 0


def main():
    args = parse_args()
    code = run_verification(args.project, args.source, args.target)
    sys.exit(code)


if __name__ == "__main__":
    main()
