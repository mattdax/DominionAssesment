import unittest
from datetime import datetime
from scripts.telemetryGenerator import Asset
from scripts.timeToEntry import AssetAnalysis
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

def createAsset(
    assetId: str,
    longitude: float,
) -> Asset:
    return Asset(
        assetId=assetId,
        assetType="public",
        longitude=longitude,
        latitude=45.4215,
        sequence=1,
        heading=90.0,
        speed=20.0,
        timestamp="2026-07-17T12:00:00.000+00:00",
    )


def createAnalysis(
    assetId: str,
    isInsideZone: bool,
) -> AssetAnalysis:
    return AssetAnalysis(
        assetId=assetId,
        isInsideZone=isInsideZone,
        nearestZoneId="zone-1",
        distanceToZone=(
            0.0 if isInsideZone else 100.0
        ),
        entryZoneId=(
            "zone-1"
            if isInsideZone
            else None
        ),
        tte=(
            0.0 if isInsideZone else None
        ),
        threatLevel=(
            "critical"
            if isInsideZone
            else "normal"
        ),
    )


class TestAutonomousDroneController(unittest.TestCase):
    def setUp(self):
        self.controller = AutonomousDroneController(
            startLong=-75.6972,
            startLat=45.4215,
            patrolSpeed=50.0,
            tolerance=5.0,
            interceptSpeed=90.0,
            shadowDistance=50.0
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
    
    def test_no_valid_target_returns_none(self):
        selected = self.controller.selectTarget([],{},)

        self.assertIsNone(selected)

        outsideAsset = createAsset("drone:outside", -75.6962)

        outsideAnalysis = createAnalysis(outsideAsset.assetId,False)

        selected = self.controller.selectTarget([outsideAsset],
        {
            outsideAsset.assetId:
            outsideAnalysis
        })

        self.assertIsNone(selected)
    def test_inside_asset_is_selected(self):
        insideAsset = createAsset("drone:inside",-75.6962)

        selected = self.controller.selectTarget([insideAsset],
            {insideAsset.assetId:createAnalysis(insideAsset.assetId,True)})

        self.assertIs(selected, insideAsset)
    
    def test_nearest_inside_asset_is_selected(self):
        farAsset = createAsset("drone:far",-75.6500)

        nearAsset = createAsset("drone:near",-75.6962)

        selected = self.controller.selectTarget(
        [farAsset,nearAsset],
        {
            farAsset.assetId:
                createAnalysis(farAsset.assetId,True),
            nearAsset.assetId:
                createAnalysis(nearAsset.assetId,True),
        }
    )

        self.assertIs(selected, nearAsset)