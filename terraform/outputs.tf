output "ingestion_sa_email" {
  value = google_service_account.ingestion_sa.email
}

output "transform_sa_email" {
  value = google_service_account.transform_sa.email
}
