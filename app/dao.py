import hashlib
from app.models import User, Airport, SeatRoleEnum, Flight, Route, Aircraft, UserRoleEnum,Policy, StopAirport, Seat, Booking, Ticket, Payment
from app import db, dao
from sqlalchemy import cast, Date, func
from datetime import datetime, time


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

def get_policy(policy_id=None):
    p = Policy.query
    if policy_id:
        p.filter(Policy.id.__eq__(policy_id))

    return p.first()


def add_stopairport(stop_airport, flight_id, airport_id):
    sa = StopAirport(airport_id=airport_id, flight_id=flight_id, note=stop_airport.get('note'), stop_time=stop_airport.get('stop_time'))
    if sa:
        db.session.add(sa)
        db.session.commit()
    return sa

def get_stop_airport(flight_id):
    stop_airports = StopAirport.query
    if flight_id:
        stop_airports = stop_airports.filter(StopAirport.flight_id.__eq__(flight_id))
    return stop_airports.all()

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


def get_airport(airport_id=None, kw = None):
    airports = Airport.query
    if kw:
        airports = airports.filter((Airport.name + " " + Airport.location).contains(kw))
    if airport_id:
        airports = airports.filter(Airport.id.__eq__(airport_id)).first()
        return airports

    return airports.all()


def get_seat(aircraft_id = None):
    seats = Seat.query
    if aircraft_id:
        seats = seats.filter(Seat.aircraft.__eq__(aircraft_id))
    return seats.all()


def count_booking():
    return db.session.query(Booking.id).count()

def add_booking(booking = None):
    booking_id = f'B{count_booking():09d}'
    b = Booking(flight_id=booking.get('flight_id'),customer_id=booking.get('customer_id'), id=booking_id, first_name= booking.get('first_name'),last_name = booking.get('last_name'),dob= booking.get('dob'),sex= booking.get('sex'),phone_number= booking.get('phone_number'),citizen_id= booking.get('citizen_id'),email= booking.get('email'),booking_date = datetime.today())

    if b:
        db.session.add(b)
        db.session.commit()
    return b

def get_booking(booking_id = None):
    booking = Booking.query

    if booking_id:
        return booking.filter(Booking.id.__eq__(booking_id)).first()

    return booking.all()
def add_ticket(ticket = None, payment_id = None):
    ticket_id = f'T{count_booking():09d}'
    tk = Ticket(id=ticket_id, booking_id = ticket.get('booking_id'), fly_date=ticket.get('fly_date'), seat_id=ticket.get('seat_number'), price=ticket.get('price'))

    if tk:
        booking = get_booking(booking_id=ticket.get('booking_id'))
        booking.status = True
        booking.payment_id = payment_id
        db.session.add(tk)
        db.session.commit()
    return tk

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

def get_flights(flight_id = None, route_id = None, start_date = None, is_available = None):
    flights = Flight.query

    if route_id:
        flights = flights.filter(Flight.route.__eq__(route_id), Flight.departure_time.cast(Date) == start_date)
    if flight_id:
        flights = flights.filter(Flight.id.__eq__(flight_id)).first()
        return flights
    if is_available:
        flights = flights.filter(Flight.departure_time > datetime.today())

    return flights.all()


def count_payment():
    return db.session.query(Payment.id).count()

def add_payment(payment = None):
    id = f'T{count_payment():09d}'
    p = Payment(id=id,card_number=payment.get('card_number'), expire_date=payment.get('expire_date'), cvv_code=payment.get('cvv_code'))

    if p:
        db.session.add(p)
        db.session.commit()
        return p


# def get_available_seat(flight_id = None):
#     if flight_id:
#         seat = db.session.query(Booking.flight_id).join(Ticket, Ticket.seat_id)


def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


def stats_revenue_flight(flight_id = None):

    stats = (db.session.query(Booking.flight_id, func.sum(Ticket.price).label('total_price'))
            .join(Flight, Booking.flight_id == Flight.id)
            .join(Ticket, Ticket.booking_id == Booking.id))
    if flight_id:
        stats = (stats.filter(Booking.status == 1, Booking.flight_id.__eq__(flight_id))
            .group_by(Booking.flight_id))
    return (stats.filter(Booking.status == 1)
            .group_by(Booking.flight_id).all())


def stats_revenue_route(from_date = None, to_date = None):
    query = (db.session.query(Route.id, Route.name, func.count(Flight.id), func.sum(Ticket.price).label('total_price'))
    .join(Flight, Flight.route == Route.id)
    .join(Booking, Booking.flight_id == Flight.id)
    .join(Ticket, Ticket.booking_id == Booking.id))
    if from_date != None and to_date != None:
        query = query.filter(Flight.departure_time.cast(Date) >= from_date, Flight.departure_time.cast(Date) <= to_date)
    return ( query.group_by(Route.id).all())



def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, time):
        return obj.strftime('%H:%M:%S')
    else:
        raise TypeError("Type not serializable")