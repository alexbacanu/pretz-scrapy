/* Instances */
resource "oci_core_instance" "tf_free_instance_db" {
  #Required
  availability_domain = data.oci_identity_availability_domain.ad.name
  compartment_id      = var.compartment_ocid
  shape               = var.instance_shape_a1

  #Optional
  display_name = "tf-free-instance-db"

  shape_config {
    #Optional
    ocpus         = 2
    memory_in_gbs = 12
  }

  create_vnic_details {
    #Optional
    subnet_id        = oci_core_subnet.tf_free_subnet.id
    assign_public_ip = true
    display_name     = "tf-free-vnic-db"
    hostname_label   = "tf-free-instance-db"
  }

  source_details {
    source_type = "image"
    source_id   = lookup(data.oci_core_images.compute_a1_images.images[0], "id")
  }

  instance_options {
    #Optional
    are_legacy_imds_endpoints_disabled = true
  }

  metadata = {
    ssh_authorized_keys = file(var.public_key_path)
  }
}

resource "oci_core_instance" "tf_free_instance_scrapy" {
  #Required
  availability_domain = data.oci_identity_availability_domain.ad.name
  compartment_id      = var.compartment_ocid
  shape               = var.instance_shape_e2

  #Optional
  display_name = "tf-free-instance-scrapy"

  shape_config {
    #Optional
    ocpus         = 2
    memory_in_gbs = 12
  }

  create_vnic_details {
    #Optional
    subnet_id        = oci_core_subnet.tf_free_subnet.id
    assign_public_ip = true
    display_name     = "tf-free-vnic-scrapy"
    hostname_label   = "tf-free-instance-scrapy"
  }

  source_details {
    source_type = "image"
    source_id   = lookup(data.oci_core_images.compute_e2_images.images[0], "id")
  }

  instance_options {
    #Optional
    are_legacy_imds_endpoints_disabled = true
  }

  metadata = {
    ssh_authorized_keys = file(var.public_key_path)
  }
}
