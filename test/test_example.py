import unittest
from app import app


class TestExample(unittest.TestCase):

    def test_starter(self): 
        tester = app.test_client()
        response = tester.get('/healthcheck')
        self.assertEqual(response.status_code, 200)
