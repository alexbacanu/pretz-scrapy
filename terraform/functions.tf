## MAIN ##
# Declare local values
locals {
  timestamp = formatdate("YYMMDDhhmmss", timestamp())
}

# Compress source code
data "archive_file" "source" {
  type        = "zip"
  source_dir  = "../scrapy/"
  output_path = "/tmp/function-${local.timestamp}.zip"
}

# Create bucket that will host the souce code
resource "google_storage_bucket" "bucket" {
  name     = "${var.project}-function"
  location = var.region
}

# Add source code zip to bucket
resource "google_storage_bucket_object" "zip" {
  # Append file MD5 to force bucket to be recreated
  name   = "source.zip#${data.archive_file.source.output_md5}"
  bucket = google_storage_bucket.bucket.name
  source = data.archive_file.source.output_path
}

# Create database for functions (Just once per project)
# resource "google_app_engine_application" "emag_database" {
#   project       = var.project
#   location_id   = var.region
#   database_type = "CLOUD_FIRESTORE"
# }




## FUNCTIONS ##
# Create Cloud Function for Sitemap
resource "google_cloudfunctions_function" "sitemap_function" {
  name    = var.function_sitemap_name
  runtime = "python39"

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.sitemap-topic.name
  }

  available_memory_mb = 512
  timeout             = 540
  max_instances       = 4
  entry_point         = var.function_sitemap_entry_point

  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.zip.name

  environment_variables = {
    SCRAPERAPI_KEY = var.SCRAPERAPI_KEY
  }
}

# Create Cloud Function for Products
resource "google_cloudfunctions_function" "products_function" {
  name    = var.function_products_name
  runtime = "python39"

  available_memory_mb = 512
  timeout             = 540
  max_instances       = 4
  trigger_http        = true
  entry_point         = var.function_products_entry_point

  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.zip.name

  environment_variables = {
    SCRAPERAPI_KEY = var.SCRAPERAPI_KEY
  }
}




## IAM ##
# IAM entry for a single user to invoke the function
resource "google_cloudfunctions_function_iam_member" "sitemap_invoker" {
  project        = google_cloudfunctions_function.sitemap_function.project
  region         = google_cloudfunctions_function.sitemap_function.region
  cloud_function = google_cloudfunctions_function.sitemap_function.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}

# IAM entry for a single user to invoke the function
resource "google_cloudfunctions_function_iam_member" "products_invoker" {
  project        = google_cloudfunctions_function.products_function.project
  region         = google_cloudfunctions_function.products_function.region
  cloud_function = google_cloudfunctions_function.products_function.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}




## APIS ##
# Enable Cloud Functions API
resource "google_project_service" "cf" {
  project = var.project
  service = "cloudfunctions.googleapis.com"

  disable_dependent_services = true
  disable_on_destroy         = false
}

# Enable Cloud Build API
resource "google_project_service" "cb" {
  project = var.project
  service = "cloudbuild.googleapis.com"

  disable_dependent_services = true
  disable_on_destroy         = false
}

# Enable Firestore API
resource "google_project_service" "fs" {
  project = var.project
  service = "firestore.googleapis.com"

  disable_dependent_services = true
  disable_on_destroy         = false
}


