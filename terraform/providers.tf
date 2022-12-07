# Oracle provider
provider "oci" {
  tenancy_ocid         = var.tenancy_ocid
  user_ocid            = var.user_ocid
  private_key_path     = var.private_key_path
  private_key_password = var.private_key_password
  fingerprint          = var.fingerprint
  region               = var.region
}

