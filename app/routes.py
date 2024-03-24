from flask import render_template, send_from_directory
from werkzeug.utils import safe_join
from app import app
import os

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/blog/<post_id>')
def post(post_id):
    post_path = safe_join(app.root_path, 'static', 'blog_posts', f'{post_id}.txt')
    if os.path.exists(post_path):
        with open(post_path, 'r') as file:
            content = file.read()
        return render_template('post.html', content=content)
    else:
        return "Post not found", 404
