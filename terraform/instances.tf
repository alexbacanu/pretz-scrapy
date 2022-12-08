/* Instances */
resource "oci_core_instance" "tf_free_instance_db" {
  #Required
  availability_domain = data.oci_identity_availability_domain.ad3.name
  compartment_id      = var.compartment_ocid
  shape               = var.instance_shape_a1

  #Optional
  display_name = "tf-free-instance-db"

  agent_config {
    plugins_config {
      desired_state = "ENABLED"
      name          = "Vulnerability Scanning"
    }
  }

  shape_config {
    #Optional
    ocpus         = 1
    memory_in_gbs = 5
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

  is_pv_encryption_in_transit_enabled = "true"

  metadata = {
    ssh_authorized_keys = file(var.ssh_public_key)
    user_data           = base64encode(templatefile(var.update_script_db, {}))
  }
}

resource "oci_core_volume_backup_policy_assignment" "tf_free_instance_db_backup" {
  #Required
  asset_id  = oci_core_instance.tf_free_instance_db.boot_volume_id
  policy_id = oci_core_volume_backup_policy.tf_free_backup_policy.id
}

output "tf_free_instance_db_ip" {
  value = oci_core_instance.tf_free_instance_db.public_ip
}

resource "oci_core_instance" "tf_free_instance_scrapy_01" {
  #Required
  availability_domain = data.oci_identity_availability_domain.ad3.name
  compartment_id      = var.compartment_ocid
  shape               = var.instance_shape_e2

  #Optional
  display_name = "tf-free-instance-scrapy"

  agent_config {
    plugins_config {
      desired_state = "ENABLED"
      name          = "Vulnerability Scanning"
    }
  }

  shape_config {
    #Optional
    ocpus         = 1
    memory_in_gbs = 1
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

  is_pv_encryption_in_transit_enabled = "true"

  metadata = {
    ssh_authorized_keys = file(var.ssh_public_key)
    user_data           = base64encode(templatefile(var.update_script_scrapy, {}))
  }
}

resource "oci_core_volume_backup_policy_assignment" "tf_free_instance_scrapy_01_backup" {
  #Required
  asset_id  = oci_core_instance.tf_free_instance_scrapy_01.boot_volume_id
  policy_id = oci_core_volume_backup_policy.tf_free_backup_policy.id
}

output "tf_free_instance_scrapy_01_ip" {
  value = oci_core_instance.tf_free_instance_scrapy_01.public_ip
}
