terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# --- BigQuery Datasets ---

resource "google_bigquery_dataset" "staging" {
  dataset_id  = "staging"
  description = "Staging Area - Raw data landing zone"
  location    = var.location
}

resource "google_bigquery_dataset" "warehouse" {
  dataset_id  = "warehouse"
  description = "Data Warehouse - Cleaned and normalized data"
  location    = var.location
}

resource "google_bigquery_dataset" "marts" {
  dataset_id  = "marts"
  description = "Data Marts - Dimensional models for BI"
  location    = var.location
}

# --- Service Accounts ---

resource "google_service_account" "ingestion_sa" {
  account_id   = "sa-ingestion"
  display_name = "Service Account for Data Ingestion"
}

resource "google_service_account" "transform_sa" {
  account_id   = "sa-transform"
  display_name = "Service Account for dbt Transformations"
}

# --- IAM Bindings (simplified) ---

resource "google_project_iam_member" "ingestion_bq_editor" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.ingestion_sa.email}"
}

resource "google_project_iam_member" "ingestion_bq_job" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.ingestion_sa.email}"
}

resource "google_project_iam_member" "transform_bq_editor" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.transform_sa.email}"
}

resource "google_project_iam_member" "transform_bq_job" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.transform_sa.email}"
}
