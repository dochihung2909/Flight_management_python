from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime, Double
from sqlalchemy.orm import relationship
from app import db, app
import enum


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2
    EMPLOYEE = 3


class SeatRoleEnum(enum.Enum):
    ECONOMY = 1
    BUSINESS = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(String(50), primary_key=True)


class Account(BaseModel, UserMixin):
    __tablename__ = 'account'

    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    user = relationship('User', backref='account', uselist=False)
    account_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)


class User(BaseModel):
    __tablename__ = 'user'

    name = Column(String(50), nullable=False)
    dob = Column(DateTime)
    sex = Column(Boolean)
    phone_number = Column(String(50))
    email = Column(String(50))
    address = Column(String(50))
    account_id = Column(String(50), ForeignKey(Account.id), nullable=False)
    customer = relationship('Customer', backref='customer')
    administrator = relationship('Administrator', backref='administrator')
    employee = relationship('Employee', backref='employee')


class Customer(db.Model):
    __tablename__ = 'customer'

    id = Column(String(50), ForeignKey(User.id), primary_key=True)
    identify_id = Column(String(20))
    nation = Column(String(50))
    invoice = relationship('Invoice', backref='invoice')
    e_ticket = relationship('ETicket', backref='e_ticket')
    ticket = relationship('Ticket', backref='ticket')


class Administrator(db.Model):
    __tablename__ = 'administrator'

    id = Column(String(50), ForeignKey(User.id), primary_key=True)
    work_place = Column(String(50))
    report = relationship('ReportRevenue', backref='report_revenue')


class Employee(db.Model):
    __tablename__ = 'employee'

    id = Column(String(50), ForeignKey(User.id), primary_key=True)
    work_place = Column(String(50))
    schedule = relationship('Schedule', backref='schedule')
    invoice = relationship('Invoice', backref='invoice')


class Invoice(db.Model):
    __tablename__ = 'invoice'

    id = Column(String(50), primary_key=True)
    date_created = Column(DateTime, nullable=False)
    customer_id = Column(String(50), ForeignKey(User.id), nullable=False)
    employee_id = Column(String(50), ForeignKey(User.id), nullable=False)
    total_price = Column(Double)
    note = Column(String(50))
    details = relationship('Invoice_Details', backref='detail', uselist=False)


class InvoiceDetails(db.Model):
    __tablename__ = 'invoice_details'

    id = Column(String(50), primary_key=True)
    invoice_id = Column(String(50), ForeignKey(Invoice.id), nullable=False)
    e_ticket = relationship('ETicket', backref='e_ticket')


class ETicket(db.Model):
    __tablename__ = 'e_ticket'

    id = Column(String(50), primary_key=True)
    status = Column(Boolean)
    date_booked = Column(DateTime)
    customer_id = Column(String(50), ForeignKey(Customer.id), nullable=False)
    tickets = relationship('Ticket', backref='tickets')
    invoice_details = Column(String(50), ForeignKey(InvoiceDetails.id), nullable=False)


class Airline(db.Model):
    __tablename__ = 'airline'

    id = Column(String(50), primary_key=True)
    airline_name = Column(String(50))
    tickets = relationship('Ticket', backref='tickets')


class TicketPrice(db.Model):
    __tablename__ = 'ticket_price'

    id = Column(String(50), primary_key=True)
    price = Column(Integer)
    discount = Column(Integer)
    ticket = relationship('Ticket', backref='ticket')


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
    route = relationship('Route', backref='route')
    stop_airport = relationship('StopAirport', backref='stop_airport')


class ReportRevenue(db.Model):
    __tablename__ = 'report_revenue'

    id = Column(String(50), primary_key=True)
    total_revenue = Column(Double)
    report_time = Column(DateTime)
    time_created = Column(DateTime)
    detail_report = relationship('DetailsReportRevenue', backref='details_report_revenue')
    administrator = Column(String(50), ForeignKey(Administrator.id), nullable=False)


class DetailsReportRevenue(db.Model):
    __tablename__ = 'details_report_revenue'

    id = Column(String(50), primary_key=True)
    report_id = Column(String(50), ForeignKey(ReportRevenue.id))
    routes = relationship('Route', backref='routes')


class Route(db.Model):
    __tablename__ = 'route'

    id = Column(String(50), primary_key=True)
    departure_airport = Column(String(50), ForeignKey(Airport.id))
    arrival_airport = Column(String(50), ForeignKey(Airport.id))
    report_id = Column(String(50), ForeignKey(DetailsReportRevenue.id))


class Flight(db.Model):
    __tablename__ = 'flight'

    id = Column(String(50), primary_key=True)
    flight_date = Column(DateTime)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    schedule = relationship('Schedule', backref='schedule')
    route = Column(String(50), ForeignKey(Route.id), nullable=False)
    stop_airport = relationship('StopAirport', backref='stop_airport')
    ticket = relationship('Ticket', backref='ticket')
    aircraft = Column(String(50), ForeignKey(Aircraft.id), nullable=False)


class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = Column(String(50), primary_key=True)
    fly_date = Column(DateTime)
    seat = relationship('Seat', backref='seat', uselist=False)
    platform = Column(String(50))
    e_ticket_id = Column(String(50), ForeignKey(ETicket.id), nullable=False)
    airline_id = Column(String(50), ForeignKey(Airline.id), nullable=False)
    ticket_price = Column(String(50), ForeignKey(TicketPrice.id), nullable=False)
    customer = Column(String(50), ForeignKey(Customer.id), nullable=False)
    flight = Column(String(50), ForeignKey(Flight.id), nullable=False)


class Seat(db.Model):
    __tablename__ = 'seat'

    id = Column(String(50), primary_key=True)
    name = Column(String(10))
    type = Column(Enum(SeatRoleEnum), default=SeatRoleEnum.ECONOMY)
    ticket = Column(String(50), ForeignKey(Ticket.id), nullable=False)
    aircraft = Column(String(50), ForeignKey(Aircraft.id), nullable=False)


class Schedule(db.Model):
    __tablename__ = 'schedule'

    id = Column(String(50), primary_key=True)
    employee_id = Column(String(50), ForeignKey(Employee.id))
    flight_id = Column(String(50), ForeignKey(Flight.id))


class StopAirport(db.Model):
    __tablename__ = 'stop_airport'

    id = Column(String(50), ForeignKey(Airport.id), primary_key=True)
    minimum_time = Column(Integer)
    maximum_time = Column(Integer)
    note = Column(String(50))
    flight_id = Column(String(50), ForeignKey(Flight.id), nullable=False)
    airport_id = Column(String(50), ForeignKey(Airport.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
