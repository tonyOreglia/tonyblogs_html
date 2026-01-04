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
        | jq '.meta' \
        > "metadata/${filename}.json"
}

for mdfile in markdown/*.md; do
    filename=$(basename "$mdfile" .md)

    convert_to_html "$mdfile" "$filename"
    extract_post_metadata "$mdfile" "$filename"
done
