from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, DateTime, Double, Time
from sqlalchemy.orm import relationship
from app import db, app
import enum
import datetime


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
    dob = Column(DateTime)
    sex = Column(Boolean)
    phone_number = Column(String(50))
    citizen_id = Column(String(50))
    email = Column(String(50))
    address = Column(String(50))
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.CUSTOMER)
    invoices = relationship('Invoice', backref='employee_invoice')
    ticket = relationship('Ticket', backref='customer_ticket')
    e_ticket = relationship('ETicket', backref='customer_eticket')
    employee_schedule = relationship('Schedule', backref='employee_schedule')


class Invoice(BaseModel):
    __tablename__ = 'invoice'

    date_created = Column(DateTime, nullable=False)
    employee_id = Column(String(50), ForeignKey(User.id), nullable=False)
    note = Column(String(50))
    details = relationship('InvoiceDetails', backref='invoice_detail', uselist=False)

    def __repr__(self):
        return '<Invoice: {}>'.format(self.id)


class InvoiceDetails(BaseModel):
    __tablename__ = 'invoice_details'

    invoice_id = Column(String(50), ForeignKey(Invoice.id), nullable=False)
    total_price = Column(Double)
    quantity = Column(Integer)


class ETicket(BaseModel):
    __tablename__ = 'e_ticket'

    status = Column(Boolean)
    date_booked = Column(DateTime)
    customer_id = Column(String(50), ForeignKey(User.id), nullable=False)
    tickets = relationship('Ticket', backref='eticket_tickets')


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


class Route(BaseModel):
    __tablename__ = 'route'

    departure_airport_id = Column(String(50), ForeignKey(Airport.id))
    arrival_airport_id = Column(String(50), ForeignKey(Airport.id))
    departure_airport = relationship('Airport', foreign_keys=[departure_airport_id])
    arrival_airport = relationship('Airport', foreign_keys=[arrival_airport_id])


class Flight(BaseModel):
    __tablename__ = 'flight'

    departure_time = Column(DateTime)
    time_flight = Column(Time)
    economy_seats = Column(Integer)
    business_seats = Column(Integer)
    route = Column(String(50), ForeignKey(Route.id), nullable=False)
    aircraft = Column(String(50), ForeignKey(Aircraft.id), nullable=False)
    schedule = relationship('Schedule', backref='flight_schedule', uselist=False)
    stop_airport = relationship('StopAirport', backref='flight_stop_airport')
    ticket = relationship('Ticket', backref='flight_ticket')


class Seat(BaseModel):
    __tablename__ = 'seat'

    name = Column(String(10))
    type = Column(Enum(SeatRoleEnum), default=SeatRoleEnum.ECONOMY)
    aircraft = Column(String(50), ForeignKey(Aircraft.id), nullable=False)
    ticket = relationship('Ticket', backref='seat_ticket', uselist=False)


class Ticket(BaseModel):
    __tablename__ = 'ticket'

    fly_date = Column(DateTime)
    e_ticket_id = Column(String(50), ForeignKey(ETicket.id), nullable=False)
    flight_id = Column(String(50), ForeignKey(Flight.id), nullable=False)
    seat_id = Column(String(50), ForeignKey(Seat.id), nullable=False)
    customer_id = Column(String(50), ForeignKey(User.id), nullable=False)


class Schedule(BaseModel):
    __tablename__ = 'schedule'

    employee_id = Column(String(50), ForeignKey(User.id))
    flight_id = Column(String(50), ForeignKey(Flight.id))


class StopAirport(db.Model):
    __tablename__ = 'stop_airport'

    id = Column(String(50), ForeignKey(Airport.id), primary_key=True)
    minimum_time = Column(Integer)
    maximum_time = Column(Integer)
    note = Column(String(50))
    flight_id = Column(String(50), ForeignKey(Flight.id), nullable=False)
    airport_id = Column(String(50), ForeignKey(Airport.id), nullable=False)
    stop_aiport = relationship('Airport', foreign_keys=[id])
    airport = relationship('Airport', foreign_keys=[airport_id])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        import hashlib
        u1 = User(id='ADMIN00001', username='hungts', password=hashlib.md5('123456'.encode('utf-8')).hexdigest(), name='Do Chi Hung', dob='2003/09/30', sex=0, phone_number='0364623646', email='hungdo29090310@gmail.com', address='125 TMT1', user_role=UserRoleEnum.ADMIN)

        airports = [
            Airport(id='AP00001', name='Tân Sơn Nhất', location='Ho Chi Minh City'),
            Airport(id='AP00002', name='Nội Bài', location='Hà Nội'),
            Airport(id='AP00003', name='Đà Nẵng', location='Đà Nẵng'),
            Airport(id='AP00004', name='Cam Ranh', location='Khánh Hòa'),
            Airport(id='AP00005', name='Phú Quốc', location='Kiên Giang'),
            Airport(id='AP00006', name='Cần Thơ', location='Cần Thơ'),
            Airport(id='AP00007', name='Vinh', location='Nghệ An'),
            Airport(id='AP00008', name='Phù Cát', location='Bình Định'),
            Airport(id='AP00009', name='Chu Lai', location='Quảng Nam'),
            Airport(id='AP00010', name='Tuy Hòa', location='Phú Yên'),
            Airport(id='AF00001', name='Heathrow Airport', location='London, United Kingdom'),
            Airport(id='AF00002', name='Charles de Gaulle Airport', location='Paris, France'),
            Airport(id='AF00003', name='Los Angeles International Airport', location='Los Angeles, United States'),
            Airport(id='AF00004', name='Narita International Airport', location='Tokyo, Japan'),
            Airport(id='AF00005', name='Dubai International Airport', location='Dubai, United Arab Emirates'),
            Airport(id='AF00006', name='Sydney Airport', location='Sydney, Australia'),
            Airport(id='AF00007', name='Singapore Changi Airport', location='Singapore'),
            Airport(id='AF00008', name='Frankfurt Airport', location='Frankfurt, Germany'),
            Airport(id='AF00009', name='Incheon International Airport', location='Seoul, South Korea'),
            Airport(id='AF00010', name='Beijing Capital International Airport', location='Beijing, China')
        ]

        aircrafts = [
            Aircraft(id='AC00001', name='Boeing 737', manufacturer='Boeing', capacity=150),
            Aircraft(id='AC00002', name='Airbus A320', manufacturer='Airbus', capacity=160),
            Aircraft(id='AC00003', name='Boeing 777', manufacturer='Boeing', capacity=300),
            Aircraft(id='AC00004', name='Embraer E190', manufacturer='Embraer', capacity=100),
            Aircraft(id='AC00005', name='Airbus A350', manufacturer='Airbus', capacity=300),
            Aircraft(id='AC00006', name='Bombardier CRJ900', manufacturer='Bombardier', capacity=90),
            Aircraft(id='AC00007', name='Boeing 747', manufacturer='Boeing', capacity=400),
            Aircraft(id='AC00008', name='Airbus A380', manufacturer='Airbus', capacity=550),
            Aircraft(id='AC00009', name='McDonnell Douglas MD-11', manufacturer='McDonnell Douglas', capacity=290),
            Aircraft(id='AC00010', name='ATR 72', manufacturer='ATR', capacity=70)
        ]

        routes = []
        for i in range(len(airports) - 1):
            for j in range(len(airports)):
                route = Route(
                    id=f"Route_{airports[i].id}_{airports[j].id}",
                    departure_airport_id=airports[i].id,
                    arrival_airport_id=airports[j].id
                )
                routes.append(route)


        # Hiển thị các tuyến bay đã tạo
        # for route in routes:
        #     print(route.id, route.departure_airport_id, route.arrival_airport_id, next((airport for airport in airports if airport.id == route.departure_airport_id), None).name)
        db.session.add_all(airports)
        db.session.add_all(routes)
        db.session.add_all(aircrafts)
        db.session.add(u1)
        db.session.commit()

