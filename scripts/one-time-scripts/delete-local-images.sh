#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MARKDOWN_POSTS_DIR="$SCRIPT_DIR/../../markdown-posts"

# Find all image files in markdown-posts subfolders
find "$MARKDOWN_POSTS_DIR" -type f \( \
    -iname "*.png" -o \
    -iname "*.jpeg" -o \
    -iname "*.jpg" -o \
    -iname "*.gif" -o \
    -iname "*.webp" \
\) -delete


