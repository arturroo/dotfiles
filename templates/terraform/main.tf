# ==============================================================================
# Copyright (c) 2026 Artur Fejklowicz
# SPDX-License-Identifier: Apache-2.0
# Author: Artur Fejklowicz | Version: 1.0.0 | Updated: 2026-10-14
# Terraform Main Configuration
# Initializes the Google provider using project and region variables.
# ==============================================================================

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# Example: Enabling core Google Cloud APIs idempotently
resource "google_project_service" "core_apis" {
  for_each = toset([
    "run.googleapis.com",
    "secretmanager.googleapis.com",
    "aiplatform.googleapis.com",
    "cloudbuild.googleapis.com",
    "artifactregistry.googleapis.com",
  ])

  service            = each.key
  disable_on_destroy = false
}
