variable "project" {
  description = "Project ID for Google Cloud"
  type        = string
}

variable "region" {
  description = "Default GCP Region"
  type        = string
  default     = "us-central1"
}

variable "location" {
  description = "Project Location for BigQuery and GCS Bucket"
  type        = string
  default     = "US"
}

variable "gcs_bucket_name" {
  description = "Base name for the GCS Storage Bucket"
  type        = string
  default     = "de_zoomcamp_bucket"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  type        = string
  default     = "demo_dataset"
}