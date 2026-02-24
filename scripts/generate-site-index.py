#!/bin/sh

import glob
import os
import json
from datetime import datetime

posts = []

for jsonfile in glob.glob('metadata/*.json'):
    with open(jsonfile, 'r') as f:
        metadata = json.load(f)
    slug = metadata.get('slug', '')
    date_published = metadata.get('date', '')
    title = metadata.get('title', '')
    draft = metadata.get('draft', False)
    if draft:
        continue
    if slug and date_published:
        # parse date to sortable format; fallback to string if necessary
        try:
            date_obj = datetime.strptime(date_published, '%Y-%m-%dT%H:%M:%S%z')
        except Exception:
            try:
                date_obj = datetime.fromisoformat(date_published)
                if date_obj.tzinfo is None:
                    from datetime import timezone
                    date_obj = date_obj.replace(tzinfo=timezone.utc)
                else:
                    date_obj = date_obj.astimezone(datetime.timezone.utc)
            except Exception:
                print(f"Failed to parse date: {date_published} in file {jsonfile}")
                exit(1)
        posts.append({
            'slug': slug,
            'date': date_published,
            'date_obj': date_obj,
            'title': title
        })

posts.sort(key=lambda p: p['date_obj'], reverse=True)

# Generate HTML list
post_list_html = '\n        '.join(
    f'<li><span class="post-date">{post["date_obj"].strftime("%d %b, %Y")}</span><a href="/blog/posts/{post["slug"]}.html">{post["title"]}</a></li>'
    for post in posts
)

# Read index.html and replace placeholder using absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(BASE_DIR, '..', 'index-template.html')
output_path = os.path.join(BASE_DIR, '..', 'public', 'index.html')

with open(template_path, 'r') as f:
    index_content = f.read()

index_content = index_content.replace('<!-- POSTS_PLACEHOLDER -->', post_list_html)

with open(output_path, 'w') as f:
    f.write(index_content)



