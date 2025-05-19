from datetime import datetime, timezone, date
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlalchemy as sa
from werkzeug.security import check_password_hash

from app import app, db
from app.forms import LoginForm
from app.models import User, Post, Project

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if not current_user.username == 'your_username':  # Replace with your username
        abort(403)  # Forbidden

    if request.method == 'POST':
        # Handle post creation here
        title = request.form.get('title')
        content = request.form.get('content')
        # Save to database
        flash('Post created successfully!')
        return redirect(url_for('posts'))
    return render_template('create_post.html')


@app.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    if not current_user.username == 'your_username':  # Replace with your username
        abort(403)  # Forbidden

    if request.method == 'POST':
        # Handle project creation here
        title = request.form.get('title')
        description = request.form.get('description')
        # Save to database
        flash('Project created successfully!')
        return redirect(url_for('projects'))
    return render_template('create_project.html')