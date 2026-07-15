import unittest

from scripts.telemetryGenerator import TelemetryGenerator
from server.serializer import serializeAssets, serializeAsset


class TestSerializer(unittest.TestCase):
    def test_serialize_asset(self):
        gen = TelemetryGenerator(100, 10, 2)
        serialized = serializeAsset(gen.assets[0])

        self.assertIsInstance(serialized, dict)
        self.assertEqual(serialized["assetId"], gen.assets[0].assetId)
        self.assertEqual(serialized["assetType"], gen.assets[0].assetType)
        self.assertEqual(serialized["latitude"], gen.assets[0].latitude)

    def test_serialize_asset_list(self):
        gen = TelemetryGenerator(100, 10, 2)
        serialized = serializeAssets(gen.assets)

        self.assertIsInstance(serialized, list)
        self.assertEqual(len(serialized), len(gen.assets))

        for serializedAsset, asset in zip(serialized, gen.assets):
            self.assertIsInstance(serializedAsset, dict)
            self.assertEqual(serializedAsset["assetId"], asset.assetId)
            self.assertEqual(serializedAsset["assetType"], asset.assetType)
            self.assertEqual(serializedAsset["latitude"], asset.latitude)
