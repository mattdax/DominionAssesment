import unittest
from server import create_server
from server.socketHandler import socketio
from server.telemetryHandler import TelemetryHandler
from scripts.telemetryGenerator import Asset
class TestSockets(unittest.TestCase):
    def setUp(self):
        self.server = create_server()
        self.handler: TelemetryHandler = self.server.extensions["telemetry_handler"]
        self.client = socketio.test_client(self.server)
        self.addCleanup(self.cleanThreads)
    def cleanThreads(self):
       task = self.handler.task
       self.handler.stop()
       if task is not None:
            task.join(timeout=1.0)

       if self.client.is_connected():
            self.client.disconnect()

       if task is not None:
            self.assertFalse(task.is_alive())
        
    def test_socket_connect(self):
        
        response = self.client.get_received()
        snapshot = [event for event in response if event["name"]=="assets.snapshot"]
        self.assertEqual(len(snapshot),1)
        self.assertEqual(snapshot[0]["name"], "assets.snapshot")
        assets = snapshot[0]["args"][0]["assets"]
        self.assertEqual(len(assets),100)
        
    
    def test_received_updates(self):
        initialResponse = self.client.get_received()

        # Get initial assets before any updates
        snapshot = [event for event in initialResponse if event["name"] == "assets.snapshot"]
        self.assertEqual(len(snapshot),1)

        snapAssests = snapshot[0]["args"][0]["assets"]
        initialAssetsById = {asset["assetId"]:asset for asset in snapAssests}
        # Wait for update period
        socketio.sleep(self.handler.generator.updateIntervalSeconds + 0.05)
        
        # get updated assets
        response = self.client.get_received()
        updates = [
        event for event in response if event["name"] == "assets.updated"]
        
        assets = updates[0]["args"][0]
        updatedAssetsById = {
            asset["assetId"]: asset for asset in assets
        }

        # assets.update
        self.assertEqual(len(updates),2)
        self.assertEqual(updates[0]["name"], "assets.updated")
       
       # Check all assets accounted for
        self.assertEqual(len(assets),100)
        self.assertEqual(assets[0]["sequence"],1)
        # Check old and new assets are difference
        for key in initialAssetsById.keys():
            self.assertGreater(updatedAssetsById[key]["timestamp"], initialAssetsById[key]["timestamp"])
            self.assertGreater(updatedAssetsById[key]["sequence"], initialAssetsById[key]["sequence"])
            self.assertEqual(updatedAssetsById[key]["assetId"], initialAssetsById[key]["assetId"])
            self.assertNotEqual(updatedAssetsById[key]["longitude"], initialAssetsById[key]["longitude"])
            self.assertNotEqual(updatedAssetsById[key]["latitude"], initialAssetsById[key]["latitude"])
    def test_two_clients(self):
        clientTwo = socketio.test_client(self.server)
        clientOneResponse = self.client.get_received()
        clientTwoResponse = clientTwo.get_received()

        # Get initial assets before any updates
        clientOneSnapshot = [event for event in clientOneResponse if event["name"] == "assets.snapshot"]
        clientTwoSnapshot = [event for event in clientTwoResponse if event["name"] == "assets.snapshot"]
        
        self.assertEqual(len(clientOneSnapshot),1)
        self.assertEqual(len(clientTwoSnapshot),1)

        #clientTwoResponse = self.client.get_received()
        
        snapAssestsOne = clientOneSnapshot[0]["args"][0]["assets"]
        initialAssetsByIOne = {asset["assetId"]:asset for asset in snapAssestsOne}

        snapAssestsTwo = clientTwoSnapshot[0]["args"][0]["assets"]
        initialAssetsByITwo = {asset["assetId"]:asset for asset in snapAssestsTwo}
        
        # Wait for update period
        socketio.sleep(self.handler.generator.updateIntervalSeconds + 0.05)

        responseOne = self.client.get_received()
        responseTwo = clientTwo.get_received()

        updatesOne = [ event for event in responseOne if event["name"] == "assets.updated"]
        updatesTwo = [ event for event in responseTwo if event["name"] == "assets.updated"]
        
        updateAssetsOne = updatesOne[0]["args"][0]
        updateAssetsTwo = updatesOne[0]["args"][0]
        updatedAssetsByIdOne = {
            asset["assetId"]: asset for asset in updateAssetsOne
        }
        updatedAssetsByIdTwo = {
            asset["assetId"]: asset for asset in updateAssetsTwo
        }
        # Check 2 clients have same assets after an update
        for key in updatedAssetsByIdOne.keys():
            self.assertEqual(updatedAssetsByIdOne[key]["timestamp"], updatedAssetsByIdTwo[key]["timestamp"])
            self.assertEqual(updatedAssetsByIdOne[key]["sequence"], updatedAssetsByIdTwo[key]["sequence"])
            self.assertEqual(updatedAssetsByIdOne[key]["assetId"], updatedAssetsByIdTwo[key]["assetId"])
            self.assertEqual(updatedAssetsByIdOne[key]["longitude"], updatedAssetsByIdTwo[key]["longitude"])
            self.assertEqual(updatedAssetsByIdOne[key]["latitude"], updatedAssetsByIdTwo[key]["latitude"])
