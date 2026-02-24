#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Purging Cloudflare Cache for tonycodes.com"

if [[ -f "$SCRIPT_DIR/../.env" ]]; then
  set -o allexport
  source "$SCRIPT_DIR/../.env"
  set +o allexport
fi

curl -X POST "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/purge_cache" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{"hosts":["tonycodes.com"]}'

