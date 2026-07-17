from scripts.telemetryGenerator import TelemetryGenerator
from scripts.timeToEntry import returnAnalysis
from scripts.autoDrone import AutonomousDroneController
from server.serializer import serializeAssetWithAnalysis
from flask_socketio import SocketIO
from .toolHandler import ToolHandler

class TelemetryHandler:
    def __init__(self,generator: TelemetryGenerator, socketio:SocketIO, toolHandler: ToolHandler, droneController: AutonomousDroneController):
        self.generator = generator
        self.socketio = socketio
        self.toolHandler = toolHandler
        self.droneController = droneController
        self.running = False
        self.task = None
    
    # Returns current assets
    def getSnapshot(self)-> list[dict]:
        return self.getAnalyzedAssets()
    
    # Increments assets by tick and returns new assets
    def tick(self)-> list[dict]:
        self.generator.tick()
        return self.getAnalyzedAssets()
    
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

    # Background task for generator
    def _run(self)->None:
        try:
            while self.running:
                update = self.tick()
                # Emit updated assets
                self.socketio.emit("assets.updated", {"assets":update})
                # Wait for next interval
                self.socketio.sleep(self.generator.updateIntervalSeconds)
        finally:
            self.task = None
            self.running = False
    # Preforms analysis on all assets and returns them serialized
    def getAnalyzedAssets(self)->list[dict]:
        zones = self.toolHandler.getZones()
        serializedAssets = []

        for asset in self.generator.assets:
            analysis = returnAnalysis(asset,zones)
            serialized = serializeAssetWithAnalysis(asset,analysis)
            serializedAssets.append(serialized)
        return serializedAssets
            
      