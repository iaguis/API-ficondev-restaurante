# -*- coding: utf-8 -*-
import model
from DAO import DAO

def rebuild_model():
    model._Base.metadata.create_all(model._engine)
    d = DAO()

    d.signup("Luso", "luso@luso.com", "1111", "666-666")

    t1 = model.Table("4")
    t2 = model.Table("8")
    t3 = model.Table("2")
    t4 = model.Table("8")
    t5 = model.Table("4")

    p1 = model.Product("Ensalada César", "Una ensalada riquísima", "en", 8)
    p2 = model.Product("Filete César", "Un filete riquísimo", "ca", 12)
    p3 = model.Product("Pasta César", "Una pasta riquísima", "pa", 9)
    p4 = model.Product("Pizza César", "Una pizza riquísima", "pi", 15)

    session = model.loadSession()

    session.add(t1)
    session.add(t2)
    session.add(t3)
    session.add(t4)
    session.add(t5)

    session.add(p1)
    session.add(p2)
    session.add(p3)
    session.add(p4)

    session.commit()
