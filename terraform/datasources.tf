# Availability Domain
# Get a list of Availability Domains
data "oci_identity_availability_domain" "ad3" {
  compartment_id = var.tenancy_ocid
  ad_number      = 3
}

data "oci_identity_availability_domain" "ad1" {
  compartment_id = var.tenancy_ocid
  ad_number      = 1
}

# Images
# See https://docs.oracle.com/iaas/images/
data "oci_core_images" "compute_a1_images" {
  compartment_id           = var.compartment_ocid
  operating_system         = var.operating_system
  operating_system_version = var.operating_system_version
  shape                    = var.instance_shape_a1
  sort_by                  = "TIMECREATED"
  sort_order               = "DESC"
}

data "oci_core_images" "compute_e2_images" {
  compartment_id           = var.compartment_ocid
  operating_system         = var.operating_system
  operating_system_version = var.operating_system_version
  shape                    = var.instance_shape_e2
  sort_by                  = "TIMECREATED"
  sort_order               = "DESC"
}

