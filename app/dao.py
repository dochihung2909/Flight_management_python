import hashlib
from app.models import User, Airport, SeatRoleEnum, Flight, Route, Aircraft
from app import db, dao


def auth_user(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password)).first()


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

def find_route(departure_airport, arrival_airport):
    routes = Route.query

    routes = routes.filter(Route.departure_airport == departure_airport and Route.arrival_airport == arrival_airport)
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


def get_flights(route_id = None, start_date = None, end_date = None):
    flights = Flight.query()

    if route_id:
        flights = flights.filter(Flight.route.__eq__(route_id) and Flight.departure_time.__eq__(start_date) or Flight.departure_time < start_date)

    return flights.all()

