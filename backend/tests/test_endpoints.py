import unittest
import json
from server import create_server

testPath = {
    "type": "Feature",
    "id": "path-1",
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [-75.6972, 45.4215],
            [-75.6872, 45.4215],
        ],
    },
    "properties": {
        "kind": "patrol-path",
    },
}

class TestEndpoints(unittest.TestCase):
    def setUp(self):
        server = create_server()
        self.server = server.test_client()
    def test_health_endpoint(self):
        response = self.server.get("/health")
        self.assertEqual(response.status_code,200)
    def test_asset_endpoint(self):
        
        response = self.server.get("/api/assets")
    
        res = response.get_json()
        self.assertIn("assets", res)
        self.assertIsInstance(res["assets"],list)
        asset = res["assets"][0]
        self.assertIsInstance(asset, dict)
        self.assertIn("assetId", asset)

        