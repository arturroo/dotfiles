# ==============================================================================
# Terraform Input Variables
# Strictly typed with clear descriptions and defaults.
# ==============================================================================

variable "project_id" {
  type        = string
  description = "The Google Cloud Project ID where resources will be provisioned."
}

variable "region" {
  type        = string
  description = "Primary GCP region for resources."
  default     = "europe-west1"
}

variable "zone" {
  type        = string
  description = "Primary GCP zone for resources."
  default     = "europe-west1-b"
}
