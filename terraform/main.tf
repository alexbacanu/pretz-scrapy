# Set google provider settings
provider "google" {
  credentials = file(var.GOOGLE_CREDENTIALS)

  project = var.project
  region  = var.region
  zone    = var.zone
}

