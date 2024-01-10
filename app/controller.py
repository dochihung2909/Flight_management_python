from app import app, dao, models, db
from flask import render_template, request, redirect, jsonify

from flask_login import login_user

import datetime

import math


def home():
    airports = dao.get_all_airport()
    seat_types = dao.get_all_seat_type()
    print(dao.get_aircraft(kw='Boeing 737')[0])
    return render_template('frontpage.html', airports=airports, seat_types=seat_types)


def login_page():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username, password)
    if user:
        login_user(user=user)
    return redirect('/admin')


def creae_schedule():
    flight_id = f'F{dao.count_flight():05d}'

    return render_template('/em/schedule.html', airports=dao.get_all_airport(), aircrafts=dao.get_aircraft(), flight_id=flight_id)


def add_flight():
    data = request.form

    route_flight = dao.find_route(dao.get_airport(name=data.get('departure_airport'))[0], dao.get_airport(name=data.get('arrival_airport'))[0]).id
    print(route_flight)
    if route_flight:
        time_flight = datetime.time(int(data.get('flight_hours')), int(data.get('flight_minutes')))
        aircraft = dao.get_aircraft(kw=data.get('aircraft'))[0]

        business_seats = math.trunc(aircraft.capacity * (1/3))

        economy_seats = aircraft.capacity - business_seats
        flight = {
            'departure_time': data.get('departure_time'),
            'time_flight': time_flight,
            'route': route_flight,
            'aircraft': aircraft.id,
            'economy_seats': economy_seats,
            'business_seats': business_seats
        }
        print(flight)
        if dao.add_flight(flight):
            return jsonify({'status': 200})

    return jsonify({'status': 500, 'err_msg': 'Something wrong!'})