#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# create metadata directory if it does not exist
mkdir -p "$SCRIPT_DIR/../metadata"
mkdir -p "$SCRIPT_DIR/../public/posts"

find "$SCRIPT_DIR/../public/posts" -type f -delete
find "$SCRIPT_DIR/../metadata" -type f -delete
find "$SCRIPT_DIR/../public" -type f -name "index.html" -delete

convert_to_html() {
  local mdfile="$1"
  local filename="$2"
  pandoc \
    -f markdown-smart \
    -t html "$mdfile" \
    -o "$SCRIPT_DIR/../public/posts/${filename}.html" \
    --css "https://tonycodes.com/blog/style.css" \
    --standalone
}

extract_post_metadata() {
  local mdfile="$1"
  local filename="$2"

  pandoc "$mdfile" \
    -t json |
    jq --arg slug "$filename" '{date: .meta.date.c[0].c, title: ([.meta.title.c[]? | select(.t != "Space") | .c] | join(" ")), slug: $slug, series: (try (.meta.series.c[0].c | map(if .t == "Space" then " " else .c end) | join("")) catch null)}' \
      >"metadata/${filename}.json"
}

find markdown-posts -type f -name "*.md" | while read -r mdfile; do
  dirpath=$(dirname "$mdfile")
  safe_filename=$(basename "$dirpath")

  # Skip draft posts
  is_draft=$(pandoc "$mdfile" -t json | jq -r '.meta.draft.c // false')
  if [ "$is_draft" = "true" ]; then
    echo "Skipping draft: $safe_filename"
    continue
  fi

  convert_to_html "$mdfile" "$safe_filename"
  extract_post_metadata "$mdfile" "$safe_filename"
done

uv run python "$SCRIPT_DIR/generate-site-index.py"

