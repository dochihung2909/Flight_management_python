import json

from app import app, dao, models, db
from flask import render_template, request, redirect, jsonify

from flask_login import login_user

from datetime import datetime

import math


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
    flight_id = f'F{dao.count_flight():05d}'

    return render_template('/em/schedule.html', airports=dao.get_all_airport(), aircrafts=dao.get_aircraft(), flight_id=flight_id)


def add_flight():
    if request.method == 'POST':
        try:
            data = request.json
            print(data, dao.get_airport(kw=data.get('departure_airport')), dao.get_airport(kw=data.get('arrival_airport')))
            route_flight = dao.find_route(dao.get_airport(kw=data.get('departure_airport'))[0],
                                          dao.get_airport(kw=data.get('arrival_airport'))[0]).id
            print(route_flight)
            if route_flight:
                time_flight = datetime.time(int(data.get('flight_hours')), int(data.get('flight_minutes')))
                aircraft = dao.get_aircraft(kw=data.get('aircraft'))[0]
                print(aircraft)
                business_seats = math.trunc(aircraft.capacity * (1 / 3))

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
                dao.add_flight(flight)
        except Exception as ex:
            print(ex)
            return jsonify({'status': 500, 'err_msg': 'Something wrong!'})
        else:
            return jsonify({'status': 200, 'flight_id': f'F{dao.count_flight():05d}'})
    else:
        try:
            data = request.args
            print(data)
            start_date = data.get('start')
            start_date = datetime.strptime(start_date + ' 00:00:00', '%m/%d/%Y %H:%M:%S')
            departure_airport = dao.get_airport(kw=data.get('departure_airport'))[0]
            arrival_airport = dao.get_airport(kw=data.get('arrival_airport'))[0]
            route_flight = dao.find_route(departure_airport, arrival_airport).id
            print(route_flight)
            flights = dao.get_flights(route_id=route_flight, start_date=start_date)
            print(flights)
            flights = (
                [{'id': flight.id,
                  'departure_time': flight.departure_time,
                  'time_flight': flight.time_flight,
                  'departure_airport': {'name': departure_airport.name, 'location': departure_airport.location},
                  'arrival_airport': {'name': arrival_airport.name, 'location': arrival_airport.location}
                } for flight in flights])
        except Exception as ex:
            print(ex)
            return jsonify({'status': 500, 'err_msg': 'Something wrong!'})
        else:
            return jsonify({'status': 200, 'flights': json.dumps(flights, default=dao.custom_serializer)})
