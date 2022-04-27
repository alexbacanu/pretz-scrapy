# Enable Cloud Tasks API
resource "google_project_service" "ct" {
  project = var.project
  service = "cloudtasks.googleapis.com"

  disable_dependent_services = true
  disable_on_destroy         = false
}

# Create random strng
# resource "random_string" "random_suffix" {
#   length  = 8
#   special = false
#   upper   = false
# }

# Create Tasks Push Queue
resource "google_cloud_tasks_queue" "emag-sitemap-queue" {
  name     = "emag-sitemap-queue"
  location = var.region

  rate_limits {
    max_concurrent_dispatches = 4
    max_dispatches_per_second = 1
  }

  retry_config {
    max_attempts       = 18
    max_retry_duration = "120s"
    max_backoff        = "45s"
    min_backoff        = "10s"
    max_doublings      = 6
  }

  # Prevent destruction of this resource because it takes 7 days
  lifecycle {
    prevent_destroy = true
  }
}
