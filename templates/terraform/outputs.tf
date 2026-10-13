# ==============================================================================
# Copyright (c) 2026 Artur Fejklowicz
# SPDX-License-Identifier: Apache-2.0
# Author: Artur Fejklowicz | Version: 1.0.0 | Updated: 2026-10-14
# Terraform Outputs
# ==============================================================================

output "project_id" {
  description = "The target Google Cloud Project ID."
  value       = var.project_id
}

output "region" {
  description = "The default deployment region."
  value       = var.region
}
