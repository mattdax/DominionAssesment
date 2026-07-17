import unittest

from shapely.geometry import Polygon

from scripts.telemetryGenerator import Asset
from scripts.timeToEntry import (
    AssetAnalysis,
    returnAnalysis,
    zoneToPolygon,
)

testZone = {
    "type": "Feature",
    "id": "zone-1",
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [-75.70, 45.40],
            [-75.60, 45.40],
            [-75.60, 45.50],
            [-75.70, 45.50],
            [-75.70, 45.40],
        ]],
    },
    "properties": {
        "kind": "restricted-zone",
        "name": "Test zone",
    },
}

farZone = {
    "type": "Feature",
    "id": "zone-2",
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [-75.40, 45.40],
            [-75.30, 45.40],
            [-75.30, 45.50],
            [-75.40, 45.50],
            [-75.40, 45.40],
        ]],
    },
    "properties": {
        "kind": "restricted-zone",
        "name": "Far zone",
    },
}

def createTestAsset(longitude, latitude):
    return Asset(
        assetId="asset-1",
        assetType="public",
        longitude=longitude,
        latitude=latitude,
        sequence=0,
        heading=90.0,
        speed=10.0,
        timestamp="2026-01-01T00:00:00.000+00:00",
    )
class TestAssetAnalysis(unittest.TestCase):
    def test_zone_converts_to_polygon(self):
        polygon = zoneToPolygon(testZone)

        self.assertIsInstance(polygon, Polygon)
        self.assertTrue(polygon.is_valid)
    def test_no_zones_returns_normal(self):
        asset = createTestAsset(-75.65, 45.45)

        analysis = returnAnalysis(asset, [])

        self.assertIsInstance(analysis, AssetAnalysis)
        self.assertEqual(analysis.assetId, asset.assetId)
        self.assertFalse(analysis.isInsideZone)
    def test_asset_inside_zone(self):
        asset = createTestAsset(-75.65, 45.45)

        analysis = returnAnalysis(asset, [testZone])

        self.assertTrue(analysis.isInsideZone)
        self.assertEqual(analysis.nearestZoneId, "zone-1")
    def test_nearest_zone_is_selected(self):
        asset = createTestAsset(-75.75, 45.45)
        analysis = returnAnalysis(asset, [farZone, testZone])
        self.assertEqual(analysis.nearestZoneId, "zone-1")