from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime, Double
from sqlalchemy.orm import relationship
from app import db, app
import enum


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2
    EMPLOYEE = 3


class TicketRoleEnum(enum.Enum):
    ECONOMY = 1
    BUSINESS = 2


class Account(db.Model):
    id = Column(String, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    user = relationship('User', backref='account', uselist=False)
    account_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)


class User(db.Model):
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    dob = Column(DateTime)
    sex = Column(Boolean)
    phone_number = Column(String)
    address = Column(String)
    account_id = Column(String, ForeignKey(Account.id), nullable=False)


class Customer(User):
    identify_id = Column(String(20))


class Administrator(User):
    work_place = Column(String)


class Employee(User):
    work_place = Column(String)
    schedule = relationship('Schedule', backref='schedule')

class Invoice(db.Model):
    id = Column(String, primary_key=True)
    date_created = Column(DateTime, nullable=False)
    customer_name = Column(String)
    employee_name = Column(String)
    total_price = Column(Double)
    note = Column(String)
    details = relationship('Invoice_Details', backref='detail', uselist=False)


class E_Ticket(db.Model):
    id = Column(String, primary_key=True)
    status = Column(Boolean)
    date_booked = Column(DateTime)
    customer_id = Column(String, ForeignKey(Customer.id), nullable=False)
    tickets = relationship('Ticket', backref='tickets')
    details = relationship('Invoice_Details', backref='detail', uselist=False)


class Airline(db.Model):
    id = Column(String, primary_key=True)
    airline_name = Column(String)
    tickets = relationship('Ticket', backref='tickets')


class Ticket(db.Model):
    id = Column(String, primary_key=True)
    fly_date = Column(DateTime)
    ticket_role = Column(Enum(TicketRoleEnum), default=TicketRoleEnum.ECONOMY)
    seat = Column(String)
    platform = Column(String)
    e_ticket_id = Column(String, ForeignKey(E_Ticket.id), nullable=False)
    airline_id = Column(String, ForeignKey(Airline.id), nullable=False)


class TicketPrice(db.Model):
    id = Column(String, primary_key=True)
    price = Column(Integer)
    discount = Column(Integer)


class InvoiceDetails(db.Model):
    id = Column(String, primary_key=True)
    invoice_id = Column(String, ForeignKey(Invoice.id), nullable=False)
    e_ticket_id = Column(String, ForeignKey(E_Ticket.id), nullable=False)


class Flight(db.Model):
    id = Column(String, primary_key=True)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    schedule = relationship('Schedule', backref='schedule')


class Schedule(db.Model):
    id = Column(String, primary_key=True)
    employee_id = Column(String, ForeignKey(Employee.id))
    flight_id = Column(String, ForeignKey(Flight.id))


class Airport(db.Model):
    id = Column(String, primary_key=True)
    name = Column(String)
    location = Column(String)


class Aircraft(db.Model):
    id = Column(String, primary_key=True)
    name = Column(String)
    manufacturer = Column(String)
    capacity = Column(Integer)


class ReportRevenue(db.Model):
    id = Column(String, primary_key=True)
    total_revenue = Column(Double)
    report_time = Column(DateTime)


class DetailsReportRevenue(db.Model):
    id = Column(String, primary_key=True)
    report_id = Column(String, ForeignKey(ReportRevenue.id))
    routes = relationship('Route', backref='routes')


class Route(db.Model):
    id = Column(String, primary_key=True)
    departure_airport = Column(String, ForeignKey(Airport.id))
    arrival_airport = Column(String, ForeignKey(Airport.id))
    report_id = Column(String, ForeignKey(DetailsReportRevenue.id))
