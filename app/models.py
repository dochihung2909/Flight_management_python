from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, DateTime, Double
from sqlalchemy.orm import relationship
from app import db, app
import enum


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
    invoices = relationship('Invoice', backref='user_invoice')


class Invoice(BaseModel):
    __tablename__ = 'invoice'

    date_created = Column(DateTime, nullable=False)
    user_id = Column(String(50), ForeignKey(User.id), nullable=False)
    note = Column(String(50))
    details = relationship('InvoiceDetails', backref='detail', uselist=False)

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


class Airport(db.Model):
    __tablename__ = 'airport'

    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    location = Column(String(50))


class ReportRevenue(db.Model):
    __tablename__ = 'report_revenue'

    id = Column(String(50), primary_key=True)
    total_revenue = Column(Double)
    report_time = Column(DateTime)
    time_created = Column(DateTime)
    detail_report = relationship('DetailsReportRevenue', backref='details_report_revenue')
    administrator = Column(String(50), ForeignKey(User.id), nullable=False)


class DetailsReportRevenue(db.Model):
    __tablename__ = 'details_report_revenue'

    id = Column(String(50), primary_key=True)
    report_id = Column(String(50), ForeignKey(ReportRevenue.id))
    routes = relationship('Route', backref='routes')


class Route(db.Model):
    __tablename__ = 'route'

    id = Column(String(50), primary_key=True)
    departure_airport_id = Column(String(50), ForeignKey(Airport.id))
    arrival_airport_id = Column(String(50), ForeignKey(Airport.id))
    report_id = Column(String(50), ForeignKey(DetailsReportRevenue.id))
    departure_airport = relationship('Airport', foreign_keys=[departure_airport_id])
    arrival_airport = relationship('Airport', foreign_keys=[arrival_airport_id])


class Flight(BaseModel):
    __tablename__ = 'flight'

    flight_date = Column(DateTime)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    economy_seats = Column(Integer)
    business_seats = Column(Integer)
    schedule = relationship('Schedule', backref='flight_schedule', uselist=False)
    route = Column(String(50), ForeignKey(Route.id), nullable=False)
    stop_airport = relationship('StopAirport', backref='flight_stop_airport')
    ticket = relationship('Ticket', backref='flight_ticket')
    aircraft = Column(String(50), ForeignKey(Aircraft.id), nullable=False)


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

    id = Column(String(50), primary_key=True)
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

        native_airports = [
            Airport(id='AP00001', name='Tân Sơn Nhất', location='Ho Chi Minh City'),
            Airport(id='AP00002', name='Nội Bài', location='Hà Nội'),
            Airport(id='AP00003', name='Đà Nẵng', location='Đà Nẵng'),
            Airport(id='AP00004', name='Cam Ranh', location='Khánh Hòa'),
            Airport(id='AP00005', name='Phú Quốc', location='Kiên Giang'),
            Airport(id='AP00006', name='Cần Thơ', location='Cần Thơ'),
            Airport(id='AP00007', name='Vinh', location='Nghệ An'),
            Airport(id='AP00008', name='Phù Cát', location='Bình Định'),
            Airport(id='AP00009', name='Chu Lai', location='Quảng Nam'),
            Airport(id='AP00010', name='Tuy Hòa', location='Phú Yên')
        ]

        foreign_airports = [
            Airport(id='APF00001', name='Heathrow Airport', location='London, United Kingdom'),
            Airport(id='APF00002', name='Charles de Gaulle Airport', location='Paris, France'),
            Airport(id='APF00003', name='Los Angeles International Airport', location='Los Angeles, United States'),
            Airport(id='APF00004', name='Narita International Airport', location='Tokyo, Japan'),
            Airport(id='APF00005', name='Dubai International Airport', location='Dubai, United Arab Emirates'),
            Airport(id='APF00006', name='Sydney Airport', location='Sydney, Australia'),
            Airport(id='APF00007', name='Singapore Changi Airport', location='Singapore'),
            Airport(id='APF00008', name='Frankfurt Airport', location='Frankfurt, Germany'),
            Airport(id='APF00009', name='Incheon International Airport', location='Seoul, South Korea'),
            Airport(id='APF00010', name='Beijing Capital International Airport', location='Beijing, China')
        ]

        db.session.add_all(native_airports)
        db.session.add_all(foreign_airports)
        db.session.add(u1)
        db.session.commit()

