#!/bin/bash
set -e

# Configuration
PROJECT_ID=$(gcloud config get-value project)
LOCATION="US"

echo "Using Project ID: $PROJECT_ID"
echo "Location: $LOCATION"

# Dataset Naming Convention
STAGING_DATASET="staging"
WAREHOUSE_DATASET="warehouse"
MARTS_DATASET="marts"

create_dataset() {
    local dataset_name=$1
    local description=$2
    
    if bq show "$PROJECT_ID:$dataset_name" >/dev/null 2>&1; then
        echo "Dataset $dataset_name already exists. Skipping."
    else
        echo "Creating dataset $dataset_name..."
        bq mk --dataset \
            --description "$description" \
            --location "$LOCATION" \
            "$PROJECT_ID:$dataset_name"
        echo "Dataset $dataset_name created successfully."
    fi
}

# Create Datasets
create_dataset "$STAGING_DATASET" "Staging Area - Raw data landing zone"
create_dataset "$WAREHOUSE_DATASET" "Data Warehouse - Cleaned and normalized data"
create_dataset "$MARTS_DATASET" "Data Marts - Dimensional models for BI"

echo "Infrastructure setup for datasets completed."
