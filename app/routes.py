from datetime import datetime, timezone, date
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request, abort
import sqlalchemy as sa


from app import app, db


@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))
@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html', title='Home')

@app.route('/bio')
def bio():
    return render_template('bio.html', title='Bio')

@app.route('/posts')
def posts():
    # Query posts from database
    posts = Post.query.all()  # Assuming you have a Post model
    return render_template('posts.html', title='Posts', posts=posts)

@app.route('/project')
def project():
    return render_template('posts/tamagotchi.html', title='Project')

@app.route('/projects')
def projects():
    return render_template('projects.html', title='Projects')








