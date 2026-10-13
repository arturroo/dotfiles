# ==============================================================================
# Copyright (c) 2026 Artur Fejklowicz
# SPDX-License-Identifier: Apache-2.0
# Author: Artur Fejklowicz | Version: 1.0.0 | Updated: 2026-10-14
# Terraform Remote State Configuration
# Stores remote state in GCS for locking, encryption, and team collaboration.
# ==============================================================================

terraform {
  required_version = ">= 1.9.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.0"
    }
  }

  backend "gcs" {
    bucket = "af-terraform-state"
    prefix = "terraform/state"
  }
}
