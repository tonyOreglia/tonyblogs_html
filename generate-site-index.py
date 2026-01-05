
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
    title = metadata.get('title', '');
    if slug and date_published:
        # parse date to sortable format; fallback to string if necessary
        try:
            date_obj = datetime.fromisoformat(date_published)
        except Exception:
            date_obj = date_published
        posts.append({
            'slug': slug,
            'date': date_published,
            'date_obj': date_obj,
            'title': title
        })

# Sort by date descending
posts.sort(key=lambda p: p['date_obj'], reverse=True)

# Generate HTML list
post_list_html = '\n        '.join(
    f'<li><a href="/blog/posts/{post["slug"]}.html">{post["title"]}</a></li>'
    for post in posts
)

# Read index.html and replace placeholder
template_path = './index-template.html'
output_path = 'public/index.html'

with open(template_path, 'r') as f:
    index_content = f.read()

index_content = index_content.replace('<!-- POSTS_PLACEHOLDER -->', post_list_html)

with open(output_path, 'w') as f:
    f.write(index_content)



