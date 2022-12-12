# Data from .tfvars
variable "tenancy_ocid" {}
variable "user_ocid" {}
variable "private_key_path" {}
variable "private_key_password" {}
variable "fingerprint" {}
variable "region" {}
variable "compartment_ocid" {}
variable "ssh_public_key" {}
variable "mongodb_port" {}
variable "mongodb_user" {}
variable "mongodb_pass" {}

# Instance
variable "instance_shape_a1" {
  default = "VM.Standard.A1.Flex"
}
variable "instance_shape_e2" {
  default = "VM.Standard.E2.1.Micro"
}

# Scripts
variable "update_script_db" {
  default = "scripts/update_db.sh"
}

variable "update_script_scrapy" {
  default = "scripts/update_scrapy.sh"
}
