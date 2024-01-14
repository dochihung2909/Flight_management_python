import json

import requests, stripe

from app import app, dao, models, db
from app.models import UserRoleEnum, SeatRoleEnum, Policy
from flask import render_template, request, redirect, jsonify, current_app, session

from flask_login import login_user, current_user, login_required, logout_user

from datetime import datetime, time

import hashlib

import math
from flask_principal import identity_changed, Identity, AnonymousIdentity
from sqlalchemy import update



def home():
    if not current_user.is_authenticated:
        return login()
    airports = dao.get_all_airport()
    seat_types = dao.get_all_seat_type()
    return render_template('frontpage.html', airports=airports, seat_types=seat_types)


def login_page():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username, password)

    if user:
        login_user(user=user)
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
    return redirect('/admin')


def create_schedule():
    flight_id = f'F{dao.count_flight():05d}'

    return render_template('/em/schedule.html', airports=dao.get_all_airport(), aircrafts=dao.get_aircraft(), flight_id=flight_id)


def employee_page(slug):
    if not current_user.is_authenticated:
        return redirect('/em')
    if current_user.user_role != UserRoleEnum.CUSTOMER:
        if (slug == 'schedule'):
            return create_schedule()
    else:
        return render_template('/login/index.html')

    return 'You do not have permission to access this page', 403

@login_required
def employee_login():
    if current_user.is_authenticated and current_user.user_role == UserRoleEnum.EMPLOYEE:
        flights = dao.get_flights(is_available=True)

        return render_template('/em/index.html', flights=flights)
    return render_template('/login/index.html', title='Đăng nhập tài khoản nhân viên')


@login_required
def sell_ticket():
    return render_template('/em/sell_ticket.html', routes=dao.get_route())


@app.context_processor
def common_resp():
    return {
        'UserRole': UserRoleEnum,
        'Policy': dao.get_policy()
    }

def login():
    if request.method == 'POST':
        try:
            data = request.json
            print(data)
            user = dao.auth_user(data.get('username'), data.get('password'))
            if user:
                print('login')
                if data.get('isEmployee') and user.user_role != UserRoleEnum.EMPLOYEE:
                    return jsonify({'status': 403, 'message': 'Không tồn tại nhân viên'})

                login_user(user)
                identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
            else:
                return jsonify({'status': 403, 'message': 'Sai tên đăng nhập hoặc mật khẩu'})

        except Exception as ex:
            print(ex)
            return jsonify({'status': 500, 'message': 'Something Wrong'})
        else:
            if (current_user.user_role == UserRoleEnum.EMPLOYEE):
                return jsonify({'status': 200, 'route': '/em'})
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

def subscribe(user_email, email_list, api_key):
  return requests.post(
        "https://api.mailgun.net/v3/lists/"+email_list+"/members",
        auth=('api', api_key),
        data={'subscribed': True,
              'address': user_email,})


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
                    'email': data.get('email'),
                    'username': data.get('username'),
                    'password': password,
                }
                dao.add_user(user)
            else:
                return jsonify({'status': 403, 'message': 'Tên đăng nhập đã tồn tại'})
        except Exception as ex:
            print(ex)
            return jsonify({'status': 500, 'message': 'Something Wrong'})
        else:
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
            stop_airports_data = data.get('stop_airports')
            print(stop_airports_data)
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
                    'flight_id': f'F{dao.count_flight():05d}',
                    'departure_time': data.get('departure_time'),
                    'time_flight': time_flight,
                    'route': route_flight,
                    'aircraft': aircraft.id,
                    'economy_seats': economy_seats,
                    'business_seats': business_seats,
                    'economy_price': data.get('economy_price'),
                    'business_price': data.get('business_price')
                }
                print(flight)
                employee_id = current_user.id
                if dao.add_flight(flight, employee_id):
                    for stop_airport in stop_airports_data:
                        airport = dao.get_airport(kw=stop_airport.get('name'))[0]
                        print(airport.name)
                        if airport:
                            dao.add_stopairport(stop_airport, flight_id=flight.get('flight_id'), airport_id=airport.id)
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
            current_date = datetime.today()
            departure_airport = dao.get_airport(kw=data.get('departure_airport'))[0]
            arrival_airport = dao.get_airport(kw=data.get('arrival_airport'))[0]
            route_flight = dao.find_route(departure_airport, arrival_airport).id
            print(route_flight)
            fs = dao.get_flights(route_id=route_flight, start_date=start_date)
            print(fs)
            flights = []
            for flight in fs:

                f = {
                    'id': flight.id,
                    'departure_time': flight.departure_time,
                    'time_flight': flight.time_flight,
                    'departure_airport': {'name': departure_airport.name, 'location': departure_airport.location},
                    'arrival_airport': {'name': arrival_airport.name, 'location': arrival_airport.location},
                    'economy_price': flight.economy_price,
                    'business_price': flight.business_price,
                    'stop_airports': []
                }

                stop_airports = dao.get_stop_airport(flight_id=flight.id)
                if stop_airports:
                    for ap in stop_airports:
                        print(ap)
                        airport = dao.get_airport(airport_id=ap.airport_id)
                        f['stop_airports'].append({
                            'name': airport.name,
                            'location': airport.location
                        })
                print(f)
                p = dao.get_policy()
                if current_user.user_role == UserRoleEnum.CUSTOMER:
                    time_limit = p.time_book_ticket
                else:
                    time_limit = p.time_sell_ticket
                if ((flight.departure_time - current_date).total_seconds() / 3600 > time_limit):
                    flights.append(f)
        except Exception as ex:
            print(ex)
            return jsonify({'status': 500, 'err_msg': 'Something wrong!'})
        else:
            return jsonify({'status': 200, 'flights': json.dumps(flights, default=dao.custom_serializer)})



def flight_booking():
    if request.method == 'POST':
        data = request.json
        flight = dao.get_flights(flight_id=data.get('flight_id'))
        print(flight)
        if flight:
            session['flight'] = {
                'flight_id': flight.id,
                'departure_time': data.get('departure_time'),
                'departure_airport_name': data.get('departure_airport_name'),
                'departure_airport_location': data.get('departure_airport_location'),
                'arrival_airport_name': data.get('arrival_airport_name'),
                'arrival_airport_location': data.get('arrival_airport_location'),
                'arrival_time': data.get('arrival_time'),
                'aircraft': flight.aircraft,
                'business_seats': flight.business_seats,
                'economy_seats': flight.economy_seats,
                'economy_price': flight.economy_price,
                'business_price': flight.business_price
            }
            return jsonify({'status': 200, 'route': '/flight'})
    else:
        flight = session.get('flight')
        print(flight)
        if (flight):
            stop_airports = dao.get_stop_airport(flight_id=flight.get('flight_id'))
            stop_airports_info = []
            if (stop_airports):
                for ap in stop_airports:
                    airport = dao.get_airport(airport_id=ap.airport_id)
                    stop_airports_info.append({
                        'name': airport.name,
                        'location': airport.location,
                        'stop_time': ap.stop_time
                    })
            else:
                stop_airports_info = None
            aircraft = dao.get_aircraft(id=flight.get('aircraft'))
            seats = dao.get_seat(aircraft_id=aircraft.id)
            economy_seats = [s for s in seats if s.type == SeatRoleEnum.ECONOMY]
            business_seats = [s for s in seats if s.type == SeatRoleEnum.BUSINESS]
            return render_template('/flight/index.html', flight=flight, aircraft=aircraft.name, stop_airports=stop_airports_info, economy_seats=economy_seats, business_seats=business_seats)
    return 'You dont have permision to this route'


def payment():
    if request.method == 'POST':
        try:
            data = request.json
            print(data)
            print(data.get('customer_lastname'))
            if data.get('sex') == 'male':
                sex = 1
            else:
                sex = 0
            dob = datetime.strptime(data.get('customer_dob') + ' 00:00:00', '%m/%d/%Y %H:%M:%S')
            print(dob)
            booking = {
                'first_name': data.get('customer_firstname'),
                'last_name': data.get('customer_lastname'),
                'dob': dob,
                'sex': sex,
                'phone_number': data.get('customer_phonenumber'),
                'citizen_id': data.get('customer_id_number'),
                'email': data.get('customer_email'),
                'customer_id': current_user.id,
                'flight_id': data.get('flight_id')
            }
            print(booking)
            b = dao.add_booking(booking=booking)
            if b:
                session['ticket'] = {
                    'booking_id': b.id,
                    'seat_type': data.get('seat_type'),
                    'seat_number': data.get('seat_number'),
                    'user_name': data.get('customer_lastname') + " " + data.get('customer_firstname'),
                    'price': data.get('ticket_price')
                }
                return jsonify({'status': 200, 'route': '/flight/payment'})
        except Exception as ex:
            print(ex)
            return jsonify({'status': 500, 'message': 'Something went wrong'})
        else:
            return jsonify({'status': 200, 'route': '/flight/payment'})
    else:
        flight = session['flight']
        if flight:
            booking = session['ticket']
            flight['departure_time'] = dao.get_flights(flight_id=flight.get('flight_id')).departure_time
            print(booking)
            print(flight)
            if booking:
                return render_template('/flight/payment.html', flight=flight, booking=booking)
    return 'You dont have permision to this route'


def checkout():
    try:
        if request.method == 'POST':
            ticket = session['ticket']
            data = request.json

            expiry_date_python = datetime.strptime(data.get('card_expiration')[:10], "%Y-%m-%d").date()
            if (ticket):
                flight = session['flight']
                ticket['fly_date'] = flight.get('departure_time')
                print(ticket)
                print(flight)
                payment_info = {
                    'card_number': data.get('card_number'),
                    'expire_date': expiry_date_python,
                    'cvv_code': data.get('cvv_code')
                }
                p = dao.add_payment(payment_info)
                if p:
                    dao.add_ticket(ticket=ticket, payment_id=p.id)
                    print('Success')
                    session.clear()
    except Exception as ex:
        print(ex)
        return jsonify({'status': 500, 'message': 'Something went wrong'})
    else:
        return jsonify({'status': 200, 'message': 'success', 'route': '/'})

@login_required
def update_policy(policy_id):
    try:
        data = request.json
        policy = dao.get_policy(policy_id=policy_id)
        if policy:
            policy.update_from_params(data)
            db.session.commit()

    except Exception as ex:
        print(ex)
        return jsonify({'status': 500, 'err_msg': 'Something wrong!'})
    else:
        return jsonify({'status': 200})




