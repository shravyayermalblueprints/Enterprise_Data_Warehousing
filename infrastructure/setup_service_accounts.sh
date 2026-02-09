#!/bin/bash
set -e

PROJECT_ID=$(gcloud config get-value project)
echo "Using Project ID: $PROJECT_ID"

# Service Account Names
SA_INGESTION="sa-ingestion"
SA_TRANSFORM="sa-transform"

create_service_account() {
    local sa_name=$1
    local display_name=$2
    local sa_email="$sa_name@$PROJECT_ID.iam.gserviceaccount.com"

    if gcloud iam service-accounts describe "$sa_email" >/dev/null 2>&1; then
        echo "Service Account $sa_name already exists. Skipping creation."
    else
        echo "Creating Service Account $sa_name..."
        gcloud iam service-accounts create "$sa_name" \
            --display-name "$display_name"
        echo "Service Account $sa_name created."
    fi
}

assign_role() {
    local sa_name=$1
    local role=$2
    local sa_email="$sa_name@$PROJECT_ID.iam.gserviceaccount.com"

    echo "Assigning role $role to $sa_name..."
    gcloud projects add-iam-policy-binding "$PROJECT_ID" \
        --member="serviceAccount:$sa_email" \
        --role="$role" >/dev/null
}


# 1. Ingestion SA (Writes to Staging)
create_service_account "$SA_INGESTION" "Service Account for Data Ingestion"
assign_role "$SA_INGESTION" "roles/bigquery.dataEditor"
assign_role "$SA_INGESTION" "roles/bigquery.jobUser"

# 2. Transformation SA (Reads Staging, Writes to Warehouse/Marts)
create_service_account "$SA_TRANSFORM" "Service Account for dbt Transformations"
assign_role "$SA_TRANSFORM" "roles/bigquery.dataEditor"
assign_role "$SA_TRANSFORM" "roles/bigquery.jobUser"
assign_role "$SA_TRANSFORM" "roles/bigquery.user"

echo "Service Accounts setup completed."
