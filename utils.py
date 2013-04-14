from DAO import DAO
from model import Order
from datetime import datetime

def order_ready(order_id):
    d = DAO()
    o = d.session.query(Order).filter(Order.order_id == order_id).one()
    o.date_ready = datetime.now()
    d.session.commit()
    d.session.close()
