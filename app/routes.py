from datetime import datetime, timezone, date
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request, abort
import sqlalchemy as sa


from app import app, db


@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html', title='Home')

@app.route('/bio')
def bio():
    return render_template('bio.html', title='Bio')

@app.route('/posts')
def posts():
    return render_template('posts.html', title='Posts', posts=posts)

@app.route('/post')
def post():
    return render_template('posts/healthcare.html', title='Posts', posts=posts)

@app.route('/data')
def data():
    return render_template('posts/datasecurity.html', title='Posts', posts=posts)

@app.route('/project')
def project():
    return render_template('projects/tamagotchi.html', title='Project')

@app.route('/projects')
def projects():
    return render_template('projects.html', title='Projects')








