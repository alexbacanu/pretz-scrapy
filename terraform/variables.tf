# Data from .tfvars
variable "tenancy_ocid" {}
variable "user_ocid" {}
variable "private_key_path" {}
variable "private_key_password" {}
variable "fingerprint" {}
variable "region" {}
variable "compartment_ocid" {}
variable "ssh_public_key" {}

# Instance
variable "instance_shape_a1" {
  default = "VM.Standard.A1.Flex"
}
variable "instance_shape_e2" {
  default = "VM.Standard.E2.1.Micro"
}
variable "operating_system" {
  default = "Oracle Linux"
}
variable "operating_system_version" {
  default = "8"
}
