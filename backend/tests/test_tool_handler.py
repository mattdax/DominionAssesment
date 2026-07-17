import unittest

from server.toolHandler import ToolHandler

testZone = {
            "type": "Feature",
            "id": "zone-1",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-75.70, 45.40],
                    [-75.60, 45.40],
                    [-75.60, 45.50],
                    [-75.70, 45.40],
                ]],
            },
            "properties": {
                "kind": "restricted-zone",
                "name": "Test zone",
            },
        }
testPath = {
            "type": "Feature",
            "id": "path-1",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [-75.70, 45.40],
                    [-75.60, 45.50],
                ],
            },
            "properties": {
                "kind": "patrol-path",
                "name": "Test path",
            },
        }

class TestToolHandler(unittest.TestCase):
    def setUp(self):
        self.handler = ToolHandler()
    def test_initial_empty(self):
        snapshot = self.handler.getSnapshot()
        self.assertEqual(snapshot, {
            "zones": [],
            "patrolPaths": [],
            "activePatrolPathId": None,
        })
    def test_insert_zone(self):
        self.handler.insertZone(testZone)

        snapshot = self.handler.getSnapshot()
        self.assertEqual(snapshot["zones"], [testZone])
    def test_insert_path(self):
        self.handler.insertPath(testPath)
        snapshot = self.handler.getSnapshot()
        self.assertEqual(snapshot["patrolPaths"], [testPath])
    def test_remove_zone(self):
        self.handler.insertZone(testZone)

        snapshot = self.handler.getSnapshot()
        self.assertEqual(snapshot["zones"], [testZone])
        self.handler.removeZone(testZone["id"])
        snapshot = self.handler.getSnapshot()
        self.assertEqual(snapshot["zones"], [])
    def test_remove_path(self):
        self.handler.insertPath(testPath)
        snapshot = self.handler.getSnapshot()
        self.assertEqual(snapshot["patrolPaths"], [testPath])
        self.handler.removePath(testPath["id"])
        snapshot = self.handler.getSnapshot()
        self.assertEqual(snapshot["patrolPaths"], [])
    def test_set_active_patrol_path(self):
        
        self.handler.insertPath(testPath)
        self.handler.setActivePatrolPath("path-1")
        self.assertEqual(
            self.handler.getSnapshot()["activePatrolPathId"],"path-1")


