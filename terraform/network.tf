/* Network */
resource "oci_core_vcn" "tf_free_vcn" {
  #Required
  compartment_id = var.compartment_ocid

  #Optional
  display_name = "tf-free-vcn"
  dns_label    = "tffreevcn"
  cidr_block   = "10.1.0.0/16"
}

# Subnet
resource "oci_core_subnet" "tf_free_subnet" {
  #Required
  cidr_block     = "10.1.20.0/24"
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.tf_free_vcn.id

  #Optional
  display_name      = "tf-free-subnet"
  dns_label         = "tffreesubnet"
  security_list_ids = [oci_core_security_list.tf_free_security_list.id]
  route_table_id    = oci_core_route_table.tf_free_route_table.id
  dhcp_options_id   = oci_core_vcn.tf_free_vcn.default_dhcp_options_id
}

# Internet Gateway
resource "oci_core_internet_gateway" "tf_free_internet_gateway" {
  #Required
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.tf_free_vcn.id

  #Optional
  display_name = "tf-free-internet-gateway"
}

# Public Route Table
resource "oci_core_route_table" "tf_free_route_table" {
  #Required
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.tf_free_vcn.id

  #Optional
  display_name = "tf-free-route-table"

  route_rules {
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_internet_gateway.tf_free_internet_gateway.id
  }
}

# Security List
resource "oci_core_security_list" "tf_free_security_list" {
  #Required
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.tf_free_vcn.id

  #Optional
  display_name = "tf-free-security-list"

  # Allow TCP(6) for all ips
  egress_security_rules {
    protocol    = "6"
    destination = "0.0.0.0/0"
  }

  # Allow TCP(6) port 22 for all ips
  ingress_security_rules {
    #Required
    protocol = "6"
    source   = "0.0.0.0/0"

    tcp_options {
      #Optional
      max = "22"
      min = "22"
    }
  }

  # Allow ICMP(1) type 3 code 4 for all ips
  ingress_security_rules {
    #Required
    protocol = "1"
    source   = "0.0.0.0/0"

    icmp_options {
      #Required
      type = "3"

      #Optional
      code = "4"
    }
  }

  # Allow ICMP(1) type 3 for 10.0.0.0-10.1.255.255
  ingress_security_rules {
    #Required
    protocol = "1"
    source   = "10.0.0.0/15"

    icmp_options {
      #Required
      type = "3"
    }
  }

  # Allow TCP(6) port var.mongodb_port for all ips
  ingress_security_rules {
    #Required
    protocol = "6"
    source   = "0.0.0.0/0"

    tcp_options {
      #Optional
      max = var.mongodb_port
      min = var.mongodb_port
    }
  }
}
