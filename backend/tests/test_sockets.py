import unittest
from server import create_server
from server.socketHandler import socketio
from server.telemetryHandler import TelemetryHandler
class TestSockets(unittest.TestCase):
    def setUp(self):
        self.server = create_server()
        self.handler: TelemetryHandler = self.server.extensions["telemetry_handler"]
        self.client = socketio.test_client(self.server)
    def tearDown(self):
       task = self.handler.task
       self.handler.stop()
       self.client.disconnect()
       if task is not None:
            task.join(timeout=1.0)

       if self.client.is_connected():
            self.client.disconnect()

       if task is not None:
            self.assertFalse(task.is_alive())
        
    def test_socket_connect(self):
        response = self.client.get_received()
        self.assertEqual(len(response),1)
        self.assertEqual(response[0]["name"], "assets.snapshot")
        assets = response[0]["args"][0]["assets"]
        self.assertEqual(len(assets),100)
    def test_received_updates(self):
        response = self.client.get_received()
        self.assertEqual(len(response),1)
        self.assertEqual(response[0]["name"], "assets.snapshot")
        