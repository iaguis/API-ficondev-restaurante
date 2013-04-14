# -*- coding: utf-8 -*-
from bottle import route, request, run
from DAO import DAO

@route("/login/<email>/<password>", method="POST")
def login(email='', password=''):
    return dao.login(email, password)

@route("/logout/<session_id>")
def logout(session_id=''):
    return dao.logout(session_id)

@route("/signup/<name>/<email>/<password>/<telephone>", method="POST")
def signup(name='', email='', password='', telephone=''):
    return dao.signup(name, email, password, telephone)

@route("/neworder/<session_id>", method="POST")
def neworder(session_id=''):
    json_order = request.forms.get("order")
    return dao.neworder(session_id, json_order)

@route("/reserve/<session_id>/<day>/<time_of_day>/<seats_needed>", method="POST")
def reserve_post(session_id='', day='', time_of_day='', seats_needed=''):
    return dao.reserve(session_id, day, time_of_day, seats_needed)

@route("/reserve/<session_id>/<day>/<time_of_day>", method="GET")
def reserve_get(session_id='', day='', time_of_day=''):
    dao.renew_session()
    return dao.show_tables(session_id, day, time_of_day)

@route("/listproducts/<session_id>")
def listproducts(session_id=''):
    dao.renew_session()
    return dao.list_products(session_id)

#@route("/pendingorders/<session_id>")
#def pendingorders(session_id=''):
    #dao.renew_session()
    #return dao.pending_orders(session_id)

#@route("/readyorders/<session_id>/<since>")
#def readyorders(session_id='', since=''):
    #dao.renew_session()
    #return dao.ready_orders(session_id, since)

#@route("/orders/<session_id>")
#def orders(session_id=''):
    #dao.renew_session()
    #return dao.orders(session_id)

#@route("/pickedorders/<session_id>/<since>")
#def pickedorders(session_id='', since=''):
    #dao.renew_session()
    #return dao.picked_orders(session_id, since)

dao = DAO()
run (host='localhost', port=8080, debug=True)
