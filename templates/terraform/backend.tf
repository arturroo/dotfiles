# ==============================================================================
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
