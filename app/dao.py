import hashlib
from app.models import User, Airport, SeatRoleEnum, Flight, Route, Aircraft, UserRoleEnum
from app import db, dao
from sqlalchemy import cast, Date
import datetime, time


def auth_user(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password)).first()


def is_username_available(username):
    return User.query.filter(User.username.__eq__(username)).first()

def get_all_airport():
    airports = Airport.query
    return airports.all()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_all_seat_type():
    seat_types = [e.name for e in SeatRoleEnum]
    return seat_types


def add_flight(flight):
    if flight:
        flight_id = f'F{dao.count_flight():05d}'
        f = Flight(id=flight_id, departure_time=flight.get('departure_time'), time_flight=flight.get('time_flight'), economy_seats=flight.get('economy_seats'), business_seats=flight.get('business_seats'), route=flight.get('route'), aircraft=flight.get('aircraft'))
        db.session.add(f)
        db.session.commit()
        return f


def get_all_route():
    routes = Route.query
    return routes.all()

def find_route(departure_airport = None, arrival_airport = None, id = None):
    routes = Route.query
    if (departure_airport and arrival_airport):
        routes = routes.filter(Route.departure_airport == departure_airport, Route.arrival_airport == arrival_airport)
    if id:
        routes = routes.filter(Route.id.__eq__(id))

    return routes.all()[0]


def get_aircraft(kw = None):
    aircrafts = Aircraft.query

    if kw:
        aircrafts = aircrafts.filter(Aircraft.name.__eq__(kw))

    return aircrafts.all()


def get_airport(kw = None):
    airports = Airport.query
    if kw:
        airports = airports.filter((Airport.name + " " + Airport.location).contains(kw))

    return airports.all()


def count_flight():
    return db.session.query(Flight.id).count()


def count_user():
    return db.session.query(User.id).count()


def add_user(user, role = None):
    u = User(name=user.get('name'),id=user.get('user_id'), username=user.get('username'), password=user.get('password'))
    if role:
        u.user_role = role
    db.session.add(u)
    db.session.commit()

    return u

def get_flights(route_id = None, start_date = None, end_date = None):
    flights = Flight.query

    if route_id:
        flights = flights.filter(Flight.route.__eq__(route_id), Flight.departure_time.cast(Date) == start_date)

    return flights.all()


def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def custom_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, datetime.time):
        return obj.strftime('%H:%M:%S')
    else:
        raise TypeError("Type not serializable")