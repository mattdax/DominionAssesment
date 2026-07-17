import unittest
from datetime import datetime

from scripts.autoDrone import (
    AutonomousDrone,
    AutonomousDroneController,
)

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

class TestAutonomousDroneController(unittest.TestCase):
    def setUp(self):
        self.controller = AutonomousDroneController(
            startLong=-75.6972,
            startLat=45.4215,
            patrolSpeed=20.0,
            tolerance=5.0,
        )
    def test_controller_returns_drone(self):
        drone = self.controller.getSnapshot()

        self.assertIsInstance(
            drone,
            AutonomousDrone,
        )
    def test_initial_drone_state(self):
        drone = self.controller.getSnapshot()

        self.assertEqual(
            drone.assetId,
            "auto:1",
        )
        self.assertEqual(
            drone.assetType,
            "autonomous",
        )
        self.assertEqual(drone.mode, "idle")
        self.assertEqual(drone.speed, 0.0)
    def test_drone_moves_on_active_path(self):
    # First tick activates the path.
        self.controller.tick(1.0, testPath,[],{})

        before = self.controller.getSnapshot()

        # Second tick performs movement.
        after = self.controller.tick(1.0,testPath,[],{},)

        self.assertNotEqual((before.longitude, before.latitude,),
                            (after.longitude, after.latitude,))

        self.assertEqual(after.mode, "patrol")
        self.assertEqual(after.sequence,before.sequence + 1,)