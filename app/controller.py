import json

from app import app, dao, models, db
from app.models import UserRoleEnum
from flask import render_template, request, redirect, jsonify, current_app, session

from flask_login import login_user, current_user, login_required, logout_user

from datetime import datetime, time

import hashlib

import math
from flask_principal import identity_changed, Identity, AnonymousIdentity



def home():
    airports = dao.get_all_airport()
    seat_types = dao.get_all_seat_type()
    print(dao.is_username_available('thina'))
    return render_template('frontpage.html', airports=airports, seat_types=seat_types)


def login_page():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username, password)
    identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))
    if user:
        login_user(user=user)
    return redirect('/admin')


def create_schedule():
    flight_id = f'F{dao.count_flight():05d}'

    return render_template('/em/schedule.html', airports=dao.get_all_airport(), aircrafts=dao.get_aircraft(), flight_id=flight_id)


@login_required
def employee_page(slug):
    if current_user.user_role != UserRoleEnum.CUSTOMER:
        if (slug == 'schedule'):
            return create_schedule()

    return 'You do not have permission to access this page', 403


@app.context_processor
def common_resp():
    return {
        'UserRole': UserRoleEnum
    }

def login():
    if request.method == 'POST':
        try:
            data = request.json
            print(data)
            user = dao.auth_user(data.get('username'), data.get('password'))
            print(user)
            if user:
                print('login')
                login_user(user)
                identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

        except Exception as ex:
            print(ex)
            return jsonify({'status': 500, 'message': 'Something Wrong'})
        else:
            return jsonify({'status': 200})

    return render_template('/login/index.html')

@login_required
def logout():
    logout_user()

    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect(request.args.get('next') or '/')

def signup():
    if request.method == 'POST':
        try:
            data = request.json
            username_available = dao.is_username_available(data.get('username'))

            if username_available == None:
                user_id = f'C{dao.count_user():05d}'
                password = hashlib.md5(data.get('password').encode('utf-8')).hexdigest()

                user = {
                    'name': data.get('name'),
                    'user_id': user_id,
                    'username': data.get('username'),
                    'password': password,
                }
                print(user)
                if (dao.add_user(user)):
                    user = dao.auth_user(user.get('username'), user.get('password'))
                    if user:
                        login_user(user)
                        identity_changed.send(current_app._get_current_object(),
                                              identity=Identity(user.id))
                        redirect('/')
            else:
                return jsonify({'status': 403, 'message': 'Tên đăng nhập đã tồn tại'})
        except Exception as ex:
            print(ex)
            return jsonify({'status': 500, 'message': 'Something Wrong'})
        else:
            redirect('/')
            return jsonify({'status': 200})
    else:

        return render_template('/login/signup.html')

@login_required
def add_employee():
    try:
        data = request.json
        username_available = dao.is_username_available(data.get('username'))

        if not username_available:
            user_id = f'EMP{dao.count_user():05d}'
            password = hashlib.md5(data.get('password').encode('utf-8')).hexdigest()

            user = {
                'name': data.get('name'),
                'user_id': user_id,
                'username': data.get('username'),
                'password': password,
            }
            print(user)
            dao.add_user(user, role=UserRoleEnum.EMPLOYEE)
        else:
            return jsonify({'status': 403, 'message': 'Tên đăng nhập đã tồn tại'})
    except Exception as ex:
        print(ex)
        return jsonify({'status': 500, 'message': 'Something Wrong'})
    else:
        redirect('/')
        return jsonify({'status': 200})


def add_flight():
    if request.method == 'POST':
        try:
            data = request.json
            print(data, dao.get_airport(kw=data.get('departure_airport')), dao.get_airport(kw=data.get('arrival_airport')))
            route_flight = dao.find_route(dao.get_airport(kw=data.get('departure_airport'))[0],
                                          dao.get_airport(kw=data.get('arrival_airport'))[0]).id
            print(route_flight)
            if route_flight:
                time_flight = time(int(data.get('flight_hours')), int(data.get('flight_minutes')))
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
