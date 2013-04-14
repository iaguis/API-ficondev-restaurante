# -*- coding: utf-8 -*-
from sqlalchemy import MetaData, create_engine, Column, ForeignKey
from sqlalchemy.types import Integer, String, Float, Date, DateTime
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import UniqueConstraint
from config import SQL_PASS, SQL_USER
from datetime import datetime

_engine = create_engine('mysql+mysqldb://' + SQL_USER + ':' + SQL_PASS + '@localhost/restaurante', echo=False, pool_recycle=3600)

_Base = declarative_base(_engine)
_metadata = MetaData(bind=_engine)



class Client(_Base):
    __tablename__ = 'clients'

    client_id = Column(Integer, primary_key=True)
    name = Column(String(length=100))
    email = Column(String(length=255), unique=True)
    password = Column(String(length=200))
    telephone = Column(String(length=15))
    session_id = Column(String(length=40))

    def __init__(self, name, email, password, telephone, session_id):
        self.name = name
        self.email = email
        self.password = password
        self.telephone = telephone
        self.session_id = session_id

    def __repr__(self):
        return "<Client('%s', '%s')>" % (self.name, self.email)

class Table(_Base):
    __tablename__ = 'restaurant_table'

    table_id = Column(Integer, primary_key=True)
    seat_number = Column(Integer)

    def __init__(self, seat_number):
        self.seat_number = seat_number

    def __repr__(self):
        return "<Table('%d', '%d')>" % self.table_id, self.seat_number

class Discount(_Base):
    __tablename__ = 'discounts'

    disc_id = Column(Integer, primary_key=True)
    minAumont = Column(Integer)
    disc_amount = Column(Float)

    def __init__(self, minAmount, disc_amount):
        self.minAmount = minAmount
        self.disc_amount = disc_amount

    def __repr__(self):
        return "<Discount('%s', '%d', '%d')>" % (self.product_id, self.minAmount, self.disc_amount)

class Reservation(_Base):
    __tablename__ = 'reservation'

    reservation_id = Column(Integer, primary_key=True)
    day = Column(Date)
    time_of_day = Column(String(1))

    client_id = Column(Integer, ForeignKey('clients.client_id'))
    table_id = Column(Integer, ForeignKey('restaurant_table.table_id'))

    client = relationship("Client", backref=backref('reservation'))
    table = relationship("Table", backref=backref('reservation'))

    UniqueConstraint('day', 'time_of_day')

    def __init__(self, client_id, table_id, day, time_of_day):
        self.client_id = client_id
        self.table_id = table_id
        self.day = day
        self.time_of_day = time_of_day

class Order(_Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    client_id = Column(Integer, ForeignKey('clients.client_id'))

    client = relationship("Client", backref=backref('orders'))

    def __init__(self, date, amount):
        self.date = date
        self.amount = amount
        self.date_ordered = datetime.now()

    def __repr__(self):
        return "<Order('%d', '%s')>" % (self.order_id, self.amount)

class Product(_Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    description = Column(String(length=255))
    product_type = Column(String(length=1))
    price = Column(Float)

    def __init__(self, name, description, product_type, price):
        self.name = name
        self.description = description
        self.product_type = product_type
        self.price = price

    def __repr__(self):
        return "<Product('%s')>" % (self.name)

class Order_Line(_Base):
    __tablename__ = 'order_lines'

    order_line_id = Column(Integer, primary_key=True)

    product_id = Column(Integer, ForeignKey('products.product_id'))
    order_id = Column(Integer, ForeignKey('orders.order_id'))

    amount = Column(Integer)

    product = relationship("Product", backref=backref('order_lines'))
    order = relationship("Order", backref=backref('order_lines'))

    def __init__(self, product_id, order_id, amount):
        self.product_id = product_id
        self.order_id = order_id
        self.amount = amount

    def __repr__(self):
        return "<Order_Line('%d', '%d', '%d')>" % (self.product_id, self.order_id, self.amount)

def loadSession():
    Session = sessionmaker(bind=_engine)
    session = Session()
    return session
