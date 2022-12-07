/* Backup policy */
resource "oci_core_volume_backup_policy" "tf_free_backup_policy" {
  #Required
  compartment_id = var.compartment_ocid

  #Optional
  display_name = "tf-free-gold"
  schedules {
    #Required
    backup_type       = "INCREMENTAL"
    period            = "ONE_DAY"
    retention_seconds = 345600 # 4 days

    #Optional
    hour_of_day = 1
  }

  schedules {
    #Required
    backup_type       = "INCREMENTAL"
    period            = "ONE_WEEK"
    retention_seconds = 1209600 # 2 weeks

    #Optional
    hour_of_day = 1
    day_of_week = "MONDAY"
  }

  schedules {
    #Required
    backup_type       = "INCREMENTAL"
    period            = "ONE_MONTH"
    retention_seconds = 7891200 # 3 months

    #Optional
    hour_of_day  = 1
    day_of_month = 1
  }
}
