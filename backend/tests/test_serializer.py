import unittest
import json
from scripts.telemetryGenerator import TelemetryGenerator
from server.serialize import serializeAssets, serializeAsset

class TestSerializer(unittest.TestCase):
    def test_serialize_asset(self):
        gen = TelemetryGenerator(100,10,2)
        serialized = serializeAsset(gen.assets[0])
        self.assertIsInstance(serialized,str)
        
        
        loadedJson = json.loads(serialized)

        self.assertIsInstance(loadedJson,dict)
        self.assertEqual(loadedJson["assetId"],gen.assets[0].assetId)
        self.assertEqual(loadedJson["assetType"],gen.assets[0].assetType)
        self.assertEqual(loadedJson["latitude"],gen.assets[0].latitude)

    def test_serialize_asset_list(self):
        gen = TelemetryGenerator(100,10,2)
        serialized = serializeAssets(gen.assets)
        loadedJson = json.loads(serialized)
        for i in range(len(gen.assets)):
            
            self.assertIsInstance(loadedJson[i],dict)
            self.assertEqual(loadedJson[i]["assetId"],gen.assets[i].assetId)
            self.assertEqual(loadedJson[i]["assetType"],gen.assets[i].assetType)
            self.assertEqual(loadedJson[i]["latitude"],gen.assets[i].latitude)

