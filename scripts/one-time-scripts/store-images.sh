#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MARKDOWN_POSTS_DIR="$SCRIPT_DIR/../../markdown-posts"

# Load variables from ../../.env
if [[ -f "$SCRIPT_DIR/../../.env" ]]; then
    set -o allexport
    source "$SCRIPT_DIR/../../.env"
    set +o allexport
fi


if [[ -z "${R2_ACCOUNT_ID:-}" ]]; then
    echo "Error: R2_ACCOUNT_ID environment variable is not set"
    exit 1
fi

if [[ -z "${R2_BUCKET_NAME:-}" ]]; then
    echo "Error: R2_BUCKET_NAME environment variable is not set"
    exit 1
fi

if [[ -z "${R2_ACCESS_KEY_ID:-}" ]]; then
    echo "Error: R2_ACCESS_KEY_ID environment variable is not set"
    exit 1
fi

if [[ -z "${R2_SECRET_ACCESS_KEY:-}" ]]; then
    echo "Error: R2_SECRET_ACCESS_KEY environment variable is not set"
    exit 1
fi

if [[ -z "${R2_ENDPOINT:-}" ]]; then
    echo "Error: R2_ENDPOINT environment variable is not set"
    exit 1
fi

# Export AWS credentials for the aws cli
export AWS_ACCESS_KEY_ID="$R2_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="$R2_SECRET_ACCESS_KEY"

# Counter for uploaded files
uploaded=0
skipped=0

echo "Scanning for images in $MARKDOWN_POSTS_DIR..."

# Find all image files in markdown-posts subfolders
find "$MARKDOWN_POSTS_DIR" -type f \( \
    -iname "*.png" -o \
    -iname "*.jpeg" -o \
    -iname "*.jpg" -o \
    -iname "*.gif" -o \
    -iname "*.webp" \
\) | while read -r image_path; do
    # Get relative path from markdown-posts directory
    relative_path="${image_path#$MARKDOWN_POSTS_DIR/}"
    
    # Get the folder name (post slug) and filename
    post_folder=$(dirname "$relative_path")
    filename=$(basename "$relative_path")
    
    # Construct the S3 key (path in the bucket)
    s3_key="${filename}"
    
    echo "Uploading: $relative_path -> s3://${R2_BUCKET_NAME}/${s3_key}"
    
    # Upload to R2
    if aws s3 cp "$image_path" "s3://${R2_BUCKET_NAME}/${s3_key}" \
        --endpoint-url "$R2_ENDPOINT" \
        --only-show-errors; then
        ((uploaded++)) || true
    else
        echo "  Failed to upload: $relative_path"
    fi
done

echo ""
echo "Done! Uploaded $uploaded image(s)."

