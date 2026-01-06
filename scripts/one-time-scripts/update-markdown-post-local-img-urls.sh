#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MARKDOWN_POSTS_DIR="$SCRIPT_DIR/../../markdown-posts"

echo "Scanning for local images in $MARKDOWN_POSTS_DIR ..."

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

    echo "Processing image: $filename in post folder: $post_folder"

    # Find and replace $filename with full img URL in all .md files in post_folder
    find "$MARKDOWN_POSTS_DIR/$post_folder" -maxdepth 1 -type f -iname "*.md" | while read -r md_file; do
        echo "  Updating $md_file : replacing $filename with https://img.tonycodes.com/$filename"
        # Use sed to find and replace the local filename with new URL, in-place
        echo "  running sed -i s#${filename}#https://img.tonycodes.com/${filename}#g $md_file"
        sed -i '' "s#${filename}#https://img.tonycodes.com/${filename}#g" "$md_file"
    done
done

echo "Done updating markdown posts with new image URLs."

