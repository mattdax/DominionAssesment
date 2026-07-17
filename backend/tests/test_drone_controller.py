import unittest
from datetime import datetime

from scripts.autoDrone import (
    AutonomousDrone,
    AutonomousDroneController,
)

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
    