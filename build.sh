for mdfile in markdown/*.md; do
    filename=$(basename "$mdfile" .md)
    pandoc \
        -f markdown-smart \
        -t html "$mdfile" \
        -o "public/${filename}.html" \
        --css style.css \
        --standalone
done

npx -y prettier --write public/
