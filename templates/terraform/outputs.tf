# ==============================================================================
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
