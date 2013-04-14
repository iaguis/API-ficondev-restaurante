# -*- coding: utf-8 -*-
from model import loadSession, Client, Order, Product, Table, Reservation, Order_Line
import hashlib
from validator import REG_NICK, REG_SHA1, REG_EMAIL, checkParam
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from json_generator import json_error, json_login, json_logout, json_signup, json_reserve, json_show_tables, json_products, json_neworder
from json_generator import json_orders
from datetime import datetime
import json
import M2Crypto

class DAO:
    def __init__(self):
        self.session = loadSession()

    def renew_session(self):
        self.session.close()
        self.session = loadSession()

    def _get_random_hash (self):
        random_hash = hashlib.sha1(M2Crypto.m2.rand_bytes(2048)).hexdigest()
        return random_hash

    def login(self, email, password):
        if not checkParam(email, 50, REG_EMAIL):
            return ""

        try:
            client = self.session.query(Client).filter(Client.email == email).one()
        except NoResultFound:
            return json_error("UserOrPasswordIncorrect")
        hashed_pass = hashlib.sha1(password).hexdigest()
        if hashed_pass == client.password:
            if not client.session_id:
                session_id = self._get_random_hash()
                client.session_id = session_id
                try:
                    self.session.commit()
                except:
                    self.session.rollback()
                    return ""
            return json_login(client.session_id)
        else:
            return ""

    def logout(self, session_id):
        if not (checkParam(session_id, 40, REG_SHA1)):
            return json_error("InvalidParameter")

        client = self._get_client(session_id)
        if not client:
            return json_error("LogoutError")

        if client.session_id == session_id:
            client.session_id = ""
            try:
                self.session.commit()
            except:
                self.session.rollback()
                return json_error("Rollback")
            return json_logout()
        return json_error("LogoutError")

    def signup(self, name, email, password, telephone):
        if not (checkParam (name, 50, REG_NICK)
                and checkParam (email, 255, REG_EMAIL)):
            return json_error("InvalidParameter")

        hashed_pass = hashlib.sha1(password).hexdigest()

        new_client = Client(name=name, password=hashed_pass, email=email, telephone=telephone, session_id="")

        self.session.add(new_client)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            return json_error("ExistingUserOrEmail")
        except:
            self.session.rollback()
            return json_error("Rollback")

        return json_signup()

    def neworder(self, session_id, json_order):
        client = self._get_client(session_id)

        if not client:
            return json_error("NotLoggedIn")

        order_dict = json.loads(json_order)
        order = Order(client.client_id, datetime.now())

        self.session.add(order)
        try:
            self.session.commit()
        except:
            self.session.rollback()
            return json_error("ErrorPlacingOrder")

        for order_line in order_dict["order"]:
            product_id = order_line["product_id"]
            try:
                product = self.session.query(Product).filter(Product.product_id == product_id).one()
            except:
                self.session.rollback()
                return json_error("ProductNonExistant")

            amount = order_line["amount"]
            ol = Order_Line(product.product_id, order.order_id, amount)
            self.session.add(ol)

        try:
            self.session.commit()
        except:
            # FIXME not rollbacking new order
            self.session.rollback()
            return json_error("OrderNotPlaced")

        return json_neworder(order)

    def reserve(self, session_id, day, time_of_day, seats_needed):
        client = self._get_client(session_id)

        if not client:
            return json_error("NotLoggedIn")

        day = datetime.strptime(day, "%d-%m-%Y")

        free_table = self._get_free_table(day, time_of_day, seats_needed)

        if not free_table:
            return json_error("NoFreeTables")

        reservation = Reservation(client.client_id, free_table.table_id, day, time_of_day)

        self.session.add(reservation)

        try:
            self.session.commit()
        except:
            self.session.rollback()
            return json_error("ReservationError")

        return json_reserve(reservation)

    def show_tables(self, session_id, day, time_of_day):
        client = self._get_client(session_id)

        if not client:
            return json_error("NotLoggedIn")

        tables = self.session.query(Table).all()

        return json_show_tables(tables)

    def list_products(self, session_id):
        client = self._get_client(session_id)

        if not client:
            return json_error("NotLoggedIn")

        try:
            products = self.session.query(Product).all()
        except:
            return json_error("error")

        products_dict = { "products" : [] }

        for p in products:
            products_dict["products"].append(
                { "product_id" : p.product_id,
                  "name" : p.name,
                  "description" : p.description,
                  "price" : p.price,
                  "product_type" : p.product_type
                })

        return json_products(products_dict)

    def ready_orders(self, session_id):
        client = self._get_client(session_id)

        if not client:
            return json_error("NotLoggedIn")

        try:
            # TODO filter old orders
            ready_orders = self.session.query(Order).join(Order.client).filter(Order.date_ready != None)
        except:
            self.session.rollback()
            return json_error("ReadyOrdersError")

        return json_orders(ready_orders)

    def pending_orders(self, session_id):
        client = self._get_client(session_id)

        if not client:
            return json_error("NotLoggedIn")

        try:
            pending_orders = self.session.query(Order).join(Order.client).filter(Order.date_ready == None).all()
        except:
            return json_error("PendingOrdersError")

        return json_orders(pending_orders)

    #def orders(self, session_id):
        #distributor = self._get_distributor(session_id)

        #if not distributor:
            #return json_error("NotLoggedIn")

        #try:
            #orders = self.session.query(Order).join(Order.distributor).all()
        #except:
            #return json_error("OrdersError")

        #return json_orders(orders)

    #def picked_orders(self, session_id, since):
        #distributor = self._get_distributor(session_id)

        #if not distributor:
            #return json_error("NotLoggedIn")

        #try:
            #if since=='1':
                #picked_orders = self.session.query(Order).join(Order.distributor).filter((Order.date_picked != None) &
                                                                                    #(Order.date_ready != None) &
                                                                                    #(Order.visited_pick == False)).all()

                #for ro in picked_orders:
                    #ro.visited_pick = True
                #self.session.commit()
            #else:
                #picked_orders = self.session.query(Order).join(Order.distributor).filter((Order.date_picked != None) &
                                                                                    #(Order.date_ready != None)).all()
        #except:
            #self.session.rollback()
            #return json_error("PickedOrdersError")

        #return json_orders(picked_orders)

    def _get_client(self, session_id):
        try:
            client = self.session.query(Client).filter(Client.session_id == session_id).one()
            return client
        except:
            return None

    def _get_free_table(self, day, time_of_day, seats_needed):
        try:
            tables = self.session.query(Table).all()
        except:
            return json_error("ErrorGettingTables")

        for t in tables:
            reservation = self.session.query(Reservation).filter((Reservation.table_id == t.table_id) &
                                                                 (Reservation.day == day) &
                                                                 (Reservation.time_of_day == time_of_day)).all()

            if not reservation:
                if t.seat_number >= int(seats_needed):
                    return t

        return None


