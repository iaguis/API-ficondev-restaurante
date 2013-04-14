# -*- coding: utf-8 -*-
import json
from datetime import datetime

def json_login(session_id):
    return session_id

def json_logout():
    return "success"

def json_error(error):
    return error

def json_signup():
    return "success"

def json_reserve(reservation):
    reservation_dict = { "reservation_id" : reservation.reservation_id,
                         "day" : datetime.strftime(reservation.day, "%d-%m-%Y"),
                         "time_of_day" : reservation.time_of_day,
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

def _get_products_of_order(order, order_products):
    products_list = { "products" : [] }
    total_price = 0
    for p in order_products:
        p_dict = { "product_id" : p.product_id}
        p_dict["amount"] = p.amount
        price = (p.amount * p.product.price)
        p_dict["price"] = price
        total_price += price
        products_list["products"].append(p_dict)
    products_list["total_price"] = total_price
    return products_list, price

def json_neworder(order):
    neworder_dict = { "order_id" : order.order_id }

    products_list, price = _get_products_of_order(order, order.order_lines)

    neworder_dict["products"] = products_list

    return json.dumps(neworder_dict, ensure_ascii=False)

def json_orders(orders):
    orders_dict = {"orders" : []}
    for order in orders:
        order_dict = { "order_id" : order.order_id}
        products_list, price = _get_products_of_order(order, order.order_lines)

        order_dict["products"] = products_list
        orders_dict["orders"].append(order_dict)
    return json.dumps(orders_dict, ensure_ascii=False)
