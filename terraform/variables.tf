variable "project_id" {
  description = "The ID of the GCP project"
  type        = string
}

variable "region" {
  description = "The GCP region for resources"
  type        = string
  default     = "us-central1"
}

variable "location" {
  description = "The BigQuery location"
  type        = string
  default     = "US"
}
