# Environment
variable "SCRAPEAPI_KEY" {
  sensitive = true
}

variable "GOOGLE_CREDENTIALS" {
  sensitive = true
}

# Project
variable "project" {
  default = "honestprice-tf"
}

variable "region" {
  default = "europe-west3"
}

variable "zone" {
  default = "europe-west3-a"
}

# Functions
variable "function_sitemap_name" {
  default = "cloud_crawl_sitemap"
}

variable "function_sitemap_entry_point" {
  default = "cloud_crawl_sitemap"
}

variable "function_products_name" {
  default = "cloud_crawl_products"
}

variable "function_products_entry_point" {
  default = "cloud_crawl_products"
}
