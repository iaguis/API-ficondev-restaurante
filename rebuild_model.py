# -*- coding: utf-8 -*-
import model
from DAO import DAO

model._Base.metadata.create_all(model._engine)
d = DAO()

d.signup("Luso", "luso@luso.com", "1111", "666-666")

t1 = model.Table("4")
t2 = model.Table("8")
t3 = model.Table("2")
t4 = model.Table("8")
t5 = model.Table("4")

session = model.loadSession()

session.add(t1)
session.add(t2)
session.add(t3)
session.add(t4)
session.add(t5)

session.commit()
