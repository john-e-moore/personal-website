from flask import render_template, send_from_directory
from werkzeug.utils import safe_join
from app import app
import os
from datetime import datetime
import markdown
from .utils import compute_time_diff

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/blog')
def blog():
    blog_posts = []
    print(os.getcwd())
    for filename in os.listdir('app/static/blog_posts'):
        if filename.endswith('.md'):
            post_id, post_name, timestamp = filename[:-3].split('_')
            with open(f'app/static/blog_posts/{filename}', 'r') as f:
                content = markdown.markdown(f.read())
            time_ago = compute_time_diff(timestamp)
            date = datetime.strptime(timestamp, '%Y%m%d').strftime('%Y-%m-%d')
            blog_posts.append({
                'id': post_id, 
                'name': post_name.replace('-', ' ').title(), 
                'content': content, 
                'time_ago': time_ago,
                'date': date
            })
    return render_template('blog.html', posts=blog_posts)

@app.route('/blog/<post_id>')
def post(post_id):
    post_path = safe_join(app.root_path, 'static', 'blog_posts', f'{post_id}')
    print(f"Post path: {post_path}")
    if os.path.exists(post_path):
        with open(post_path, 'r') as file:
            content = file.read()
        return render_template('post.html', content=content)
    else:
        return "Post not found", 404
