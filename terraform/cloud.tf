# Terraform cloud
terraform {
  cloud {
    organization = "pretz"
    workspaces {
      name = "pretz-scrapy-terraform"
    }
  }

  required_providers {
    oci = {
      source  = "oracle/oci"
      version = "4.100.0"
    }
  }
}
