from datetime import datetime, timezone, date
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request
import sqlalchemy as sa
from app import app, db


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/bio')
def bio():
    return render_template('bio.html', title='Bio')

@app.route('/posts')
def posts():
    return render_template('posts.html', title='Posts')

@app.route('/projects')
def projects():
    return render_template('projects.html', title='Projects')