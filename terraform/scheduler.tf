# Enable Pub/Sub API
resource "google_project_service" "ps" {
  project = var.project
  service = "pubsub.googleapis.com"

  disable_dependent_services = true
  disable_on_destroy         = false
}

# Create PubSub Topic
resource "google_pubsub_topic" "sitemap-topic" {
  project = var.project
  name    = "sitemap-topic"

  depends_on = [
    google_project_service.ps,
  ]
}

# Enable Cloud Scheduler API
resource "google_project_service" "cs" {
  project = var.project
  service = "cloudscheduler.googleapis.com"

  disable_dependent_services = true
  disable_on_destroy         = false
}

# Create Scheduler Job
resource "google_cloud_scheduler_job" "sitemap-cron-pubsub-job" {
  project = var.project
  region  = var.region
  name    = "sitemap-cron-pubsub-job"

  schedule  = "0 8 * * *" # Every day at 08:00
  time_zone = "Europe/Bucharest"
  pubsub_target {
    topic_name = google_pubsub_topic.sitemap-topic.id
    data       = base64encode("Pub/Sub")
  }
  depends_on = [
    google_project_service.cs,
  ]
}
