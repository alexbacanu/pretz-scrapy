# Declare which Terraform providers to use
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.18.0"
    }
  }
}

provider "google" {
  credentials = file(var.GOOGLE_CREDENTIALS)

  project = var.project
  region  = var.region
  zone    = var.zone
}
