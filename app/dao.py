import hashlib
from app.models import User, Airport, SeatRoleEnum


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