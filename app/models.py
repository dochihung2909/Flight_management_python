from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, DateTime, Double, Time, Date
from sqlalchemy.orm import relationship
from app import db, app
import enum
import datetime
import sqlalchemy

class UserRoleEnum(enum.Enum):
    CUSTOMER = 1
    ADMIN = 2
    EMPLOYEE = 3


class SeatRoleEnum(enum.Enum):
    ECONOMY = 1
    BUSINESS = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(String(50), primary_key=True)


class User(BaseModel, UserMixin):
    __tablename__ = 'user'

    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.CUSTOMER)
    booking = relationship('Booking', backref='user_booking')
    flight = relationship('Flight', backref='employee_flight')


class Booking(BaseModel):

    first_name = Column(String(50))
    last_name = Column(String(50))
    dob = Column(Date)
    sex = Column(Boolean)
    phone_number = Column(String(50))
    citizen_id = Column(String(50))
    email = Column(String(50))
    booking_date = Column(DateTime)
    customer_id = Column(String(50), ForeignKey(User.id), nullable=True)
    status = Column(Boolean, default=False)
    ticket = relationship('Ticket', backref='booking_ticket')


class Aircraft(db.Model):
    __tablename__ = 'aircraft'

    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    manufacturer = Column(String(50))
    capacity = Column(Integer)
    seats = relationship('Seat', backref='seats')
    flight = relationship('Flight', backref='flight')


class Airport(BaseModel):
    __tablename__ = 'airport'

    name = Column(String(50))
    location = Column(String(50))
    stop_airport = relationship('StopAirport', backref='airport_stopairport')


class Route(BaseModel):
    __tablename__ = 'route'

    name = Column(String(500))
    departure_airport_id = Column(String(50), ForeignKey(Airport.id))
    arrival_airport_id = Column(String(50), ForeignKey(Airport.id))
    departure_airport = relationship('Airport', foreign_keys=[departure_airport_id])
    arrival_airport = relationship('Airport', foreign_keys=[arrival_airport_id])
    flight = relationship('Flight', backref='route_flight')


class Flight(BaseModel):
    __tablename__ = 'flight'

    departure_time = Column(DateTime)
    time_flight = Column(Time)
    economy_seats = Column(Integer)
    business_seats = Column(Integer)
    economy_price = Column(Double)
    business_price = Column(Double)
    route = Column(String(50), ForeignKey(Route.id), nullable=False)
    aircraft = Column(String(50), ForeignKey(Aircraft.id), nullable=False)
    employee_id = Column(String(50), ForeignKey(User.id), nullable=False)
    stop_airport = relationship('StopAirport', backref='flight_stop_airport')
    ticket = relationship('Ticket', backref='flight_ticket')


class Seat(db.Model):
    __tablename__ = 'seat'

    id = Column(String(50), primary_key=True)
    aircraft = Column(String(50), ForeignKey(Aircraft.id), primary_key=True)
    name = Column(String(10))
    type = Column(Enum(SeatRoleEnum), default=SeatRoleEnum.ECONOMY)
    ticket = relationship('Ticket', backref='seat_ticket', uselist=False)


class Ticket(BaseModel):
    __tablename__ = 'ticket'

    fly_date = Column(DateTime)
    flight_id = Column(String(50), ForeignKey(Flight.id), nullable=False)
    seat_id = Column(String(50), ForeignKey(Seat.id), nullable=False)
    booking_id = Column(String(50), ForeignKey(Booking.id), nullable=False)


class StopAirport(db.Model):
    __tablename__ = 'stop_airport'

    flight_id = Column(String(50), ForeignKey(Flight.id), primary_key=True)
    airport_id = Column(String(50), ForeignKey(Airport.id), primary_key=True)
    stop_time = Column(Integer)
    note = Column(String(500))


class Policy(BaseModel):
    __tablename__ = 'flight_policy'

    airport_number = Column(Integer)
    time_flight_limit = Column(Integer)
    stop_airport_max_number = Column(Integer)
    stop_time_minimum = Column(Integer)
    stop_time_maximum = Column(Integer)
    time_book_ticket = Column(Integer)
    time_sell_ticket = Column(Integer)


def create_seats_for_aircraft(aircraft):
    total_capacity = aircraft.capacity
    business_ratio = 1 / 3

    business_seats = int(total_capacity * business_ratio)
    economy_seats = total_capacity - business_seats

    for i in range(business_seats):
        seat = Seat(id=f'B{i+1}', name=f'B{i+1}', type=SeatRoleEnum.BUSINESS, aircraft=aircraft.id)
        db.session.add(seat)

    for i in range(economy_seats):
        seat = Seat(id=f'E{i+1}', name=f'E{i+1}', type=SeatRoleEnum.ECONOMY, aircraft=aircraft.id)
        db.session.add(seat)

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        import hashlib
        u1 = User(id='ADMIN00001', username='hungts', password=hashlib.md5('123456'.encode('utf-8')).hexdigest(), name='Do Chi Hung', user_role=UserRoleEnum.ADMIN)

        airports = [
            Airport(id='AP00001', name='Tân Sơn Nhất', location='Ho Chi Minh City'),
            Airport(id='AP00002', name='Nội Bài', location='Hà Nội'),
            Airport(id='AP00003', name='Đà Nẵng', location='Đà Nẵng'),
            Airport(id='AP00004', name='Cam Ranh', location='Khánh Hòa'),
            Airport(id='AP00006', name='Cần Thơ', location='Cần Thơ'),
            Airport(id='AF00001', name='Heathrow Airport', location='London'),
            Airport(id='AF00002', name='Charles de Gaulle Airport', location='Paris'),
            Airport(id='AF00003', name='Los Angeles International Airport', location='Los Angeles'),
            Airport(id='AF00004', name='Narita International Airport', location='Tokyo'),
            Airport(id='AF00006', name='Sydney Airport', location='Sydney'),
        ]

        aircrafts = [
            Aircraft(id='AC00001', name='Boeing 737', manufacturer='Boeing', capacity=75),
            Aircraft(id='AC00004', name='Embraer E190', manufacturer='Embraer', capacity=50),
            Aircraft(id='AC00005', name='Airbus A350', manufacturer='Airbus', capacity=100),
            Aircraft(id='AC00006', name='Bombardier CRJ900', manufacturer='Bombardier', capacity=60),
            Aircraft(id='AC00010', name='ATR 72', manufacturer='ATR', capacity=40)
        ]

        p1 = Policy(id='P00001', airport_number=10, time_flight_limit=30, stop_airport_max_number=2, stop_time_minimum=20, stop_time_maximum=30, time_book_ticket=12, time_sell_ticket=4)



        routes = []
        for i in range(len(airports) - 1):
            for j in range(len(airports)):
                if airports[i].id != airports[j].id:
                    route = Route(
                        id=f"Route_{airports[i].id}_{airports[j].id}",
                        name=f'{airports[i].location} - {airports[j].location}',
                        departure_airport_id=airports[i].id,
                        arrival_airport_id=airports[j].id
                    )
                    routes.append(route)


        # Hiển thị các tuyến bay đã tạo
        # for route in routes:
        #     print(route.id, route.departure_airport_id, route.arrival_airport_id, next((airport for airport in airports if airport.id == route.departure_airport_id), None).name)
        db.session.add(p1)
        db.session.add_all(airports)
        db.session.add_all(routes)
        db.session.add_all(aircrafts)
        db.session.add(u1)
        db.session.commit()

        for aircraft in aircrafts:
            create_seats_for_aircraft(aircraft)

