import unittest

from scripts.telemetryGenerator import TelemetryGenerator, Asset

class TestTelemetryGenerator(unittest.TestCase):
    def test_generator_returns(self):
        gen = TelemetryGenerator(100,10,2)
        self.assertEqual(gen.assets,10)
    
    def test_asset_returns(self):
        gen = TelemetryGenerator(100,10,2)
        asset = gen.assets[0]
        self.assertIsInstance(asset,Asset)
        

if __name__ == "__main__":
    unittest.main()