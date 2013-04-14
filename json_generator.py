# -*- coding: utf-8 -*-
import json
from datetime import datetime
from utils import tod

def json_login(session_id):
    return session_id

def json_logout():
    return "success"

def json_error(error):
    return error

def json_signup():
    return "success"

def json_neworder(order_id):
    return json.dumps({"order_id" : order_id}, ensure_ascii=False)

def json_reserve(reservation):
    reservation_dict = { "reservation_id" : reservation.reservation_id,
                         "day" : datetime.strftime(reservation.day, "%d-%m-%Y"),
                         "time_of_day" : tod[reservation.time_of_day],
                         "table_number" : reservation.table_id
                       }
    return json.dumps(reservation_dict, ensure_ascii=False)

def json_show_tables(tables):
    tables_dict = {"tables" : []}

    for t in tables:
        table_dict = { "table_id" : t.table_id,
                       "seats" : t.seat_number,
                     }
        if t.reservation:
            table_dict["reserved"] = True
        else:
            table_dict["reserved"] = False

    return json.dumps(tables_dict, ensure_ascii=False)

def json_products(products_dict):
    return json.dumps(products_dict, ensure_ascii=False)

#def json_orders(orders):
    #orders_dict = {"orders" : []}
    #orders_dict["server_time"] = int(round(unix_time_millis(datetime.now())))

    #for order in orders:
        #order_dict = { "order_id"     : order.order_id,
                    #"product_id"      : order.product_id,
                    #"product_name"      : order.products.name,
                    #"amount"       : order.amount,
                    #"date_ordered" : int(round(unix_time_millis(order.date_ordered))),
                    #"order_price" : order.amount * order.products.price,
                    #}

        #if order.date_ready:
            #order_dict["date_ready"] = int(round(unix_time_millis(order.date_ready)))
            #if order.date_picked:
                #order_dict["date_picked"] = int(round(unix_time_millis(order.date_picked)))
        #orders_dict["orders"].append(order_dict)
    #return json.dumps(orders_dict, ensure_ascii=False)
