import hashlib
from app.models import User, Airport, SeatRoleEnum, Flight, Route, Aircraft, UserRoleEnum,Policy, StopAirport
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


def get_route():
    return Route.query.all()

def get_policy():
    p = Policy.query.first()
    return p


def add_stopairport(stop_airport, flight_id, airport_id):
    sa = StopAirport(airport_id=airport_id, flight_id=flight_id, note=stop_airport.get('note'), stop_time=stop_airport.get('stop_time'))
    if sa:
        db.session.add(sa)
        db.session.commit()
    return sa


def add_flight(flight, employee_id):
    if flight:
        f = Flight(economy_price=flight.get('economy_price'), business_price=flight.get('business_price'),employee_id=employee_id,id=flight.get('flight_id'), departure_time=flight.get('departure_time'), time_flight=flight.get('time_flight'), economy_seats=flight.get('economy_seats'), business_seats=flight.get('business_seats'), route=flight.get('route'), aircraft=flight.get('aircraft'))
        db.session.add(f)
        db.session.commit()
        return f


def find_route(departure_airport = None, arrival_airport = None, id = None):
    routes = Route.query
    if (departure_airport and arrival_airport):
        routes = routes.filter(Route.departure_airport == departure_airport, Route.arrival_airport == arrival_airport)
    if id:
        routes = routes.filter(Route.id.__eq__(id))

    return routes.all()[0]


def get_aircraft(id = None, kw = None):
    aircrafts = Aircraft.query

    if kw:
        aircrafts = aircrafts.filter(Aircraft.name.__eq__(kw))
    if id:
        aircrafts = aircrafts.filter(Aircraft.id.__eq__(id)).first()
        return aircrafts

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

def get_flights(flight_id = None, route_id = None, start_date = None, end_date = None):
    flights = Flight.query

    if route_id:
        flights = flights.filter(Flight.route.__eq__(route_id), Flight.departure_time.cast(Date) == start_date)
    if flight_id:
        flights = flights.filter(Flight.id.__eq__(flight_id)).first()
        return flights

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