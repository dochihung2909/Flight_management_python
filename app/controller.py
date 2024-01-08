from app import app, dao, models, db
from flask import render_template, request, redirect

from flask_login import login_user


def home():
    airports = dao.get_all_airport()
    seat_types = dao.get_all_seat_type()
    return render_template('frontpage.html', airports=airports, seat_types=seat_types)


def login_page():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username, password)
    if user:
        login_user(user=user)
    return redirect('/admin')


def creae_schedule():
    return render_template('/em/schedule.html', airports=dao.get_all_airport())


def add_flight():
    data = request.json

    fligt = {
        'id': data.get('id'),
        'departure_time': data.get('departure_time'),
        'arrival_time': data.get('departure_time'),
    }

    return True