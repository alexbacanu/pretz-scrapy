# Availability Domain
# Get a list of Availability Domains
data "oci_identity_availability_domain" "ad3" {
  compartment_id = var.tenancy_ocid
  ad_number      = 3
}

data "oci_identity_availability_domain" "ad2" {
  compartment_id = var.tenancy_ocid
  ad_number      = 2
}

data "oci_identity_availability_domain" "ad1" {
  compartment_id = var.tenancy_ocid
  ad_number      = 1
}

# Images
# See https://docs.oracle.com/iaas/images/
# Oracle-Linux-8.6-aarch64-2022.12.15-0
data "oci_core_images" "compute_a1_images" {
  compartment_id           = var.compartment_ocid
  display_name             = "Oracle-Linux-8.6-aarch64-2022.12.15-0"
  # operating_system         = "Oracle Linux"
  # operating_system_version = "8"
  # shape                    = var.instance_shape_a1
  # sort_by                  = "TIMECREATED"
  # sort_order               = "DESC"
}

data "oci_core_images" "compute_e2_images" {
  compartment_id           = var.compartment_ocid
  operating_system         = "Oracle Linux"
  operating_system_version = "9"
  shape                    = var.instance_shape_e2
  sort_by                  = "TIMECREATED"
  sort_order               = "DESC"
}

