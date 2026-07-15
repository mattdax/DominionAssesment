import unittest

from scripts.telemetryGenerator import TelemetryGenerator, Asset

class TestTelemetryGenerator(unittest.TestCase):
    # Test generation occurs
    def test_generator_returns(self):
        gen = TelemetryGenerator(100,10,2)
        self.assertEqual(len(gen.assets),10)
    # Test that all assets generated are correct and exist
    def test_valid_asset_returns(self):
        gen = TelemetryGenerator(100,10,2)
        for asset in gen.assets:
            asset = gen.assets[0]
            self.assertIsInstance(asset,Asset)
            self.assertEqual(asset.type,"public")
            self.assertEqual(asset.sequence,0)
            self.assertIsInstance(asset.latitude, float)
            self.assertIsInstance(asset.longitude, float)
            self.assertIsInstance(asset.heading, float)
            self.assertIsInstance(asset.speed, float)
    
    # Test same values on 2 generators with same seed
    def test_seed_consistency(self):
        genOne = TelemetryGenerator(100,10,2)
        genTwo = TelemetryGenerator(100,10,2)
        self.assertEqual(genOne.assets[0].latitude,genTwo.assets[0].latitude)
        self.assertEqual(genOne.assets[0].longitude,genTwo.assets[0].longitude)
        self.assertEqual(genOne.assets[0].heading,genTwo.assets[0].heading)
        self.assertEqual(genOne.assets[0].speed,genTwo.assets[0].speed)
    def test_asset_update(self):
        gen = TelemetryGenerator(100,10,2)
        oldLatitude = gen.assets[0].latitude
        oldLongitude = gen.assets[0].longitude
        gen.tick()
        self.assertNotEqual(oldLatitude,gen.assets[0].latitude)
        self.assertNotEqual(oldLongitude,gen.assets[0].longitude)

    def test_generator_reset(self):
        gen = TelemetryGenerator(100,10,2)
        initialLatitude = gen.assets[0].latitude
        initialLongitude = gen.assets[0].longitude
        gen.tick()
        gen.tick()
        gen.reset()
        self.assertEqual(gen.assets[0].latitude, initialLatitude)
        self.assertEqual(gen.assets[0].longitude, initialLongitude)
if __name__ == "__main__":
    unittest.main()