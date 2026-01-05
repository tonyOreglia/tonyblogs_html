#!/bin/sh

# create metadata directory if it does not exist
mkdir -p metadata

convert_to_html() {
    local mdfile="$1"
    local filename="$2"
    pandoc \
        -f markdown-smart \
        -t html "$mdfile" \
        -o "public/posts/${filename}.html" \
        --css style.css \
        --standalone
}

extract_post_metadata() {
    local mdfile="$1"
    local filename="$2"

    pandoc "$mdfile" \
        -t json \
        | jq --arg slug "$filename" '{date: .meta.date.c[0].c, title: ([.meta.title.c[]? | select(.t != "Space") | .c] | join(" ")), slug: $slug}' \
        > "metadata/${filename}.json"
}

for mdfile in markdown/*.md; do
    filename=$(basename "$mdfile" .md)

    convert_to_html "$mdfile" "$filename"
    extract_post_metadata "$mdfile" "$filename"
done

python "$(dirname "$0")/generate-site-index.py"