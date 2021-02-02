import unittest
from project import app

class TestEndPoint(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_endpoint_with_valid_form_data(self):

        res = self.client.get("/", data={
            "league": "NFL",
            "start_date": "2020-01-12",
            "end_date": "2020-01-19"
        })

        self.assertEqual(res.status_code, 200)

    def test_endpoint_with_invalid_form_data(self):
        res = self.client.get("/", data={
            "league": "NFL",
            "start_date": "2020-01-12",
            "end_date": "2020-01-01"
        })

        self.assertEqual(res.status_code, 400)
