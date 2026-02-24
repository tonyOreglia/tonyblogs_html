# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Static HTML blog generator for [tonycodes.com/blog](https://tonycodes.com/blog). Markdown posts are converted to HTML via `pandoc`, post metadata is extracted to JSON, and a Python script assembles the `public/index.html` from a template.

## Commands

```bash
# Build: convert all markdown posts → HTML + generate index
./scripts/build.sh

# Lint: format output HTML/JSON with prettier
./scripts/lint.sh

# Deploy: rsync public/ to the server (SSH host: thinkstation-home)
./scripts/deploy.sh

# Purge Cloudflare cache (requires .env with CF_ZONE_ID and CF_API_TOKEN)
./scripts/purge-cf-cache.sh

# Full deploy pipeline (build → lint → deploy → purge cache)
./deploy-latest.sh
```

## Architecture & Data Flow

1. **Source**: Each blog post lives in `markdown-posts/<slug>/index.md` with YAML frontmatter (`title`, `date`, `draft`, `tags`).

2. **Build** (`scripts/build.sh`):
   - Iterates all `markdown-posts/*/index.md` files; the parent directory name becomes the slug.
   - `pandoc` converts each `.md` → `public/posts/<slug>.html` (standalone HTML, linked to `style.css` on CDN).
   - `pandoc` + `jq` extracts metadata → `metadata/<slug>.json` (`{date, title, slug}`).
   - Calls `scripts/generate-site-index.py` to produce `public/index.html`.

3. **Index generation** (`scripts/generate-site-index.py`):
   - Reads all `metadata/*.json`, sorts posts by date descending.
   - Injects `<li>` links into `index-template.html` at `<!-- POSTS_PLACEHOLDER -->` → writes `public/index.html`.

4. **Output** (`public/`): Contains `index.html`, `posts/*.html`, `style.css`, and `icon.png`. This entire directory is deployed via rsync.

## Adding a New Post

Create `markdown-posts/<slug>/index.md` with YAML frontmatter, then run `./scripts/build.sh`. The slug (directory name) becomes the URL path (`/blog/posts/<slug>.html`).

## Dependencies

- `pandoc` — markdown to HTML/JSON conversion
- `jq` — JSON extraction from pandoc output
- `python3` — index generation script
- `npx` / `prettier` — HTML/JSON formatting (lint step)
- `rsync` — deployment to `thinkstation-home` SSH host
- `.env` file — required for `CF_ZONE_ID` and `CF_API_TOKEN` (Cloudflare cache purge)
