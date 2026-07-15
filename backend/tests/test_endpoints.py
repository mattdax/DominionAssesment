import unittest
from server import create_server
class TestEndpoints(unittest.TestCase):
    def setUp(self):
        server = create_server()
        self.server = server.test_client()
    def test_health_endpoint(self):
        response = self.server.get("/health")
        self.assertEqual(response.status_code,200)
    