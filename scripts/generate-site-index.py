#!/bin/sh

import glob
import os
import json
import re
from datetime import datetime, timezone


def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def parse_date(date_published, jsonfile):
    try:
        date_obj = datetime.strptime(date_published, '%Y-%m-%dT%H:%M:%S%z')
    except Exception:
        try:
            date_obj = datetime.fromisoformat(date_published)
            if date_obj.tzinfo is None:
                date_obj = date_obj.replace(tzinfo=timezone.utc)
            else:
                date_obj = date_obj.astimezone(timezone.utc)
        except Exception:
            print(f"Failed to parse date: {date_published} in file {jsonfile}")
            exit(1)
    return date_obj


posts = []

for jsonfile in glob.glob('metadata/*.json'):
    with open(jsonfile, 'r') as f:
        metadata = json.load(f)
    slug = metadata.get('slug', '')
    date_published = metadata.get('date', '')
    title = metadata.get('title', '')
    draft = metadata.get('draft', False)
    series = metadata.get('series', None)
    if draft:
        continue
    if slug and date_published:
        date_obj = parse_date(date_published, jsonfile)
        posts.append({
            'slug': slug,
            'date': date_published,
            'date_obj': date_obj,
            'title': title,
            'series': series,
        })

posts.sort(key=lambda p: p['date_obj'], reverse=True)

# Separate series posts from standalone posts
series_map = {}  # series name -> list of posts
standalone_posts = []

for post in posts:
    if post['series']:
        series_name = post['series']
        series_map.setdefault(series_name, []).append(post)
    else:
        standalone_posts.append(post)

# Build index list items: one entry per series + all standalone posts
# Represent series entries as {type: 'series', series_name, series_slug, date_obj (most recent)}
index_entries = []

seen_series = set()
for post in posts:
    if post['series']:
        series_name = post['series']
        if series_name not in seen_series:
            seen_series.add(series_name)
            series_slug = slugify(series_name)
            series_posts = series_map[series_name]
            most_recent = max(series_posts, key=lambda p: p['date_obj'])
            index_entries.append({
                'type': 'series',
                'series_name': series_name,
                'series_slug': series_slug,
                'date_obj': most_recent['date_obj'],
            })
    else:
        index_entries.append({'type': 'post', **post})

# Sort combined list by date descending
index_entries.sort(key=lambda e: e['date_obj'], reverse=True)

# Generate index page list items
list_items = []
for entry in index_entries:
    date_str = entry['date_obj'].strftime('%d %b, %Y')
    if entry['type'] == 'series':
        href = f"/blog/series/{entry['series_slug']}.html"
        list_items.append(
            f'<li><span class="post-date">{date_str}</span>📚 <a href="{href}">{entry["series_name"]}</a></li>'
        )
    else:
        href = f"/blog/posts/{entry['slug']}.html"
        list_items.append(
            f'<li><span class="post-date">{date_str}</span><a href="{href}">{entry["title"]}</a></li>'
        )

post_list_html = '\n        '.join(list_items)

# Read index template and write public/index.html
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(BASE_DIR, '..', 'index-template.html')
output_path = os.path.join(BASE_DIR, '..', 'public', 'index.html')

with open(template_path, 'r') as f:
    index_content = f.read()

index_content = index_content.replace('<!-- POSTS_PLACEHOLDER -->', post_list_html)

with open(output_path, 'w') as f:
    f.write(index_content)

# Generate public/series.html
series_dir = os.path.join(BASE_DIR, '..', 'public', 'series')
os.makedirs(series_dir, exist_ok=True)

series_list_items = []
for series_name, series_posts in sorted(series_map.items()):
    series_slug = slugify(series_name)
    most_recent = max(series_posts, key=lambda p: p['date_obj'])
    date_str = most_recent['date_obj'].strftime('%d %b, %Y')
    href = f"/blog/series/{series_slug}.html"
    series_list_items.append(
        f'<li><span class="post-date">{date_str}</span><a href="{href}">{series_name}</a> ({len(series_posts)} parts)</li>'
    )

series_list_html = '\n        '.join(series_list_items)

series_index_html = f"""<!DOCTYPE html>
<html>
  <head>
    <title>Series — Tony Blogs</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta charset="UTF-8" />
    <link rel="stylesheet" href="/blog/style.css" />
    <link rel="icon" href="/blog/icon.png" type="image/png" />
  </head>
  <body>
    <main>
      <h1>series</h1>
      <nav>
        <a href="https://tonycodes.com">about-me</a>
        <a href="/blog/">Blog</a>
        <a href="/blog/series.html">series</a>
      </nav>
      <ul id="blog-post-list">
        {series_list_html}
      </ul>
    </main>
  </body>
</html>
"""

series_index_path = os.path.join(BASE_DIR, '..', 'public', 'series.html')
with open(series_index_path, 'w') as f:
    f.write(series_index_html)

# Generate public/series/<slug>.html per series
for series_name, series_posts in series_map.items():
    series_slug = slugify(series_name)
    series_posts_sorted = sorted(series_posts, key=lambda p: p['date_obj'])

    post_items = []
    for post in series_posts_sorted:
        date_str = post['date_obj'].strftime('%d %b, %Y')
        href = f"/blog/posts/{post['slug']}.html"
        post_items.append(
            f'<li><span class="post-date">{date_str}</span><a href="{href}">{post["title"]}</a></li>'
        )

    posts_html = '\n        '.join(post_items)

    detail_html = f"""<!DOCTYPE html>
<html>
  <head>
    <title>{series_name} — Tony Blogs</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta charset="UTF-8" />
    <link rel="stylesheet" href="/blog/style.css" />
    <link rel="icon" href="/blog/icon.png" type="image/png" />
  </head>
  <body>
    <main>
      <h1>{series_name}</h1>
      <nav>
        <a href="https://tonycodes.com">about-me</a>
        <a href="/blog/">Blog</a>
        <a href="/blog/series.html">series</a>
      </nav>
      <ul id="blog-post-list">
        {posts_html}
      </ul>
    </main>
  </body>
</html>
"""

    detail_path = os.path.join(series_dir, f'{series_slug}.html')
    with open(detail_path, 'w') as f:
        f.write(detail_html)
