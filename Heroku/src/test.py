import os
from app import app
import unittest
import tempfile
import json

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.login("bob", "asdf")

    def tearDown(self):
        pass

    def login(self, username, password):
        rv = self.app.post("/auth",
                data=json.dumps(dict(username=username, password=password)),
                content_type="application/json")
        data = json.loads(str(rv.data, encoding="utf-8"))
        self.access_token = data.get("access_token")


    def test_auth(self):
        rv = self.app.post("/auth",
                data=json.dumps(dict(username="bob", password="asdf")),
                content_type="application/json")
        data = json.loads(str(rv.data, encoding="utf-8"))
        assert "access_token" in data

    def test_items(self):
        self.login("bob", "asdf")
        rv = self.app.put("/item/chair",
                data='{"price": 17.34}',
                headers = {"Authorization": "JWT " + self.access_token},
                content_type="application/json")
        self.app.put("/item/table",
                data='{"price": 45.67}',
                headers = {"Authorization": "JWT " + self.access_token},
                content_type="application/json")
        self.app.put("/item/lamp",
                data='{"price": 15.12}',
                headers = {"Authorization": "JWT " + self.access_token},
                content_type="application/json")
        rv = self.app.get("/items",
                headers = {"Authorization": "JWT " + self.access_token})

        data = json.loads(str(rv.data, encoding="utf-8"))
        print(data)

if __name__ == '__main__':
    unittest.main()
