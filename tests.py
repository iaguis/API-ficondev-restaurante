import unittest
from httplib2 import Http
from urllib import urlencode
import utils
import rebuild_model

class TestAPIRestaurante(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        rebuild_model.rebuild_model()

    def test_login(self):
        resp, content = h.request("http://127.0.0.1:8080/login/luso@luso.com/1111", "POST")
        # get sha1 session id
        self.assertEqual(len(content), 40)
        resp, content = h.request("http://127.0.0.1:8080/login/luso@luso.com/1211", "POST")
        self.assertEquals(content, "")

    def test_logout(self):
        resp, content = h.request("http://127.0.0.1:8080/login/luso@luso.com/1111", "POST")
        session_id = content
        resp, content = h.request("http://127.0.0.1:8080/logout/" + session_id, "GET")
        self.assertEqual(content, "success")

    def test_signup(self):
        resp, content = h.request("http://127.0.0.1:8080/signup/Manuel/manuel@t.com/1234/666-675", "POST")
        self.assertEqual(content, "success")
        resp, content = h.request("http://127.0.0.1:8080/login/manuel@t.com/1234", "POST")
        self.assertEqual(len(content), 40)

    def test_neworder(self):
        resp, content = h.request("http://127.0.0.1:8080/login/luso@luso.com/1111", "POST")
        session_id = content
        data = dict(order="""{"order" : [{"product_id" : 1, "amount" : 1}, {"product_id" : 2, "amount" : 2}]}""")
        resp, content = h.request("http://localhost:8080/neworder/" + session_id, "POST", urlencode(data))
        expected_response = """{"order_id": 1, "products": {"total_price": 32.0, "products": [{"price": 8.0, "amount": 1, "product_id": 1}, {"price": 24.0, "amount": 2, "product_id": 2}]}}"""
        self.assertEqual(content, expected_response)

    def test_reserve(self):
        resp, content = h.request("http://127.0.0.1:8080/login/luso@luso.com/1111", "POST")
        session_id = content
        # Try to reserve a table for 20 people
        resp, content = h.request("http://localhost:8080/reserve/" + session_id + "/01-08-2013/l/20", "POST")
        expected_response = """NoFreeTables"""

        self.assertEqual(content, expected_response)

        # Try to reserve a table for 6 people
        resp, content = h.request("http://localhost:8080/reserve/" + session_id + "/01-08-2013/l/6", "POST")
        expected_response = """{"table_number": 2, "time_of_day": "l", "reservation_id": 1, "day": "01-08-2013"}"""

        self.assertEqual(content, expected_response)

    def test_listproducts(self):
        # missing test
        pass

    def test_orders(self):
        resp, content = h.request("http://127.0.0.1:8080/login/luso@luso.com/1111", "POST")
        session_id = content
        data = dict(order="""{"order" : [{"product_id" : 1, "amount" : 1}, {"product_id" : 2, "amount" : 2}]}""")
        resp, content = h.request("http://localhost:8080/neworder/" + session_id, "POST", urlencode(data))
        expected_response = """{"order_id": 2, "products": {"total_price": 32.0, "products": [{"price": 8.0, "amount": 1, "product_id": 1}, {"price": 24.0, "amount": 2, "product_id": 2}]}}"""
        self.assertEqual(content, expected_response)

        data = dict(order="""{"order" : [{"product_id" : 3, "amount" : 1}, {"product_id" : 1, "amount" : 100}]}""")
        resp, content = h.request("http://localhost:8080/neworder/" + session_id, "POST", urlencode(data))
        expected_response = """{"order_id": 3, "products": {"total_price": 809.0, "products": [{"price": 9.0, "amount": 1, "product_id": 3}, {"price": 800.0, "amount": 100, "product_id": 1}]}}"""
        self.assertEqual(content, expected_response)

        resp, content = h.request("http://localhost:8080/pendingorders/" + session_id)
        expected_response = """{"orders": [{"order_id": 1, "products": {"total_price": 32.0, "products": [{"price": 8.0, "amount": 1, "product_id": 1}, {"price": 24.0, "amount": 2, "product_id": 2}]}}, {"order_id": 2, "products": {"total_price": 32.0, "products": [{"price": 8.0, "amount": 1, "product_id": 1}, {"price": 24.0, "amount": 2, "product_id": 2}]}}, {"order_id": 3, "products": {"total_price": 809.0, "products": [{"price": 9.0, "amount": 1, "product_id": 3}, {"price": 800.0, "amount": 100, "product_id": 1}]}}]}"""
        self.assertEqual(content, expected_response)

        utils.order_ready(1)

        # TODO test pendingorders ready

if __name__ == "__main__":
    h = Http(".cache")
    unittest.main()
