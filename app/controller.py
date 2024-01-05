from app import app, dao, models, db
from flask import render_template, request, redirect

from flask_login import login_user


def home():
    return render_template('frontpage.html')


def login_page():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username, password)
    if user:
        login_user(user=user)
    return redirect('/admin')