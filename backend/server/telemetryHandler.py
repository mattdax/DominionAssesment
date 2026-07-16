from scripts.telemetryGenerator import TelemetryGenerator
from server.serializer import serializeAsset,serializeAssets
from flask_socketio import SocketIO
class TelemetryHandler:
    def __init__(self,generator: TelemetryGenerator, socketio:SocketIO):
        self.generator = generator
        self.socketio = socketio
        self.running = False
        self.task = None
    
    # Returns current assets
    def getSnapshot(self)-> list[dict]:
        return serializeAssets(self.generator.assets)
    
    # Increments assets by tick and returns new assets
    def tick(self)-> list[dict]:
        self.generator.tick()
        return serializeAssets(self.generator.assets)
    
    # Returns whether service is active
    def isRunning(self)->bool:
        return self.running
    
    # Sets service to running
    def start(self)->None:
        if self.running:
            return
        self.running = True
        self.task = self.socketio.start_background_task(self._run)


    def stop(self)->None:
        self.running = False


    def _run(self)->None:
        try:
            while self.running:
                update = self.tick()
            
                self.socketio.emit("assets.updated", update)
                self.socketio.sleep(self.generator.updateIntervalSeconds)
        finally:
            self.task = None
            self.running = False
            
      