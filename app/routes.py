from flask import render_template, send_from_directory
from werkzeug.utils import safe_join
from app import app
import os
from datetime import datetime
import markdown
from .utils import compute_time_diff

@app.route('/')
def index():
    content = []
    for filename in os.listdir('app/static/blog_posts'):
        if filename.endswith('.md'):
            post_id, post_name, timestamp = filename[:-3].split('_')
            post_name = ' '.join([ x.title() for x in post_name.split('-') ])
            date = datetime.strptime(timestamp, '%Y%m%d').strftime('%Y-%m-%d')
            content.append({
                'name': post_name,
                'link': filename, # maps to 'post_extension' in 'post' route
                'date': date
            })
    # Put blog posts in order
    content.sort(key=lambda x: x['date'], reverse=True)

    return render_template('index.html', content=content)

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/blog/<post_extension>')
def post(post_extension):
    post_path = safe_join(app.root_path, 'static', 'blog_posts', f'{post_extension}')
    print(f"Post path: {post_path}")
    if os.path.exists(post_path):
        post_id, post_name, timestamp = post_extension[:-3].split('_')
        post_name = ' '.join([ x.title() for x in post_name.split('-') ])
        with open(post_path, 'r') as file:
            body = markdown.markdown(file.read())
        time_ago = compute_time_diff(timestamp)
        date = datetime.strptime(timestamp, '%Y%m%d').strftime('%Y-%m-%d')
        content = {
            'id': post_id,
            'name': post_name,
            'body': body,
            'time_ago': time_ago,
            'date': date
        }
        return render_template('post.html', content=content)
    else:
        return "Post not found", 404
