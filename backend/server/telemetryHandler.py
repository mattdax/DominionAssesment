from scripts.telemetryGenerator import TelemetryGenerator, Asset
from scripts.timeToEntry import returnAnalysis, AssetAnalysis
from scripts.autoDrone import AutonomousDroneController
from server.serializer import serializeAssetWithAnalysis, serializeAutonomousDrone
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
        serialized, _ = self.getAnalyzedAssets()
        return serialized
    
    # Increments assets by tick and returns new assets
    def tick(self)-> list[dict]:
        updated = self.generator.tick()
        serializedAssets, analysisById = self.getAnalyzedAssets(updated)
        activePath = self.toolHandler.getActivePatrolPath()
        self.droneController.tick(elapsedSeconds=self.generator.lastElapsedSeconds, 
                                  patrolPath=activePath,assets=updated, analysisByAssetId=analysisById)
        
        
        return serializedAssets
    
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

                self.socketio.emit("autonomous-drone.updated",{"drone":self.getDroneSnapshot()})
                # Wait for next interval
                self.socketio.sleep(self.generator.updateIntervalSeconds)
        finally:
            self.task = None
            self.running = False
    # Preforms analysis on all assets and returns them serialized and grouped by id (for use in autoDrone) 
    def getAnalyzedAssets(self, assets: list[Asset])->tuple[list[dict], dict[str,AssetAnalysis]]:
        zones = self.toolHandler.getZones()
        serializedAssets = []
        analysisById = {}
        
        for asset in assets:
            analysis = returnAnalysis(asset,zones)
            analysisById[asset.assetId] = analysis
            serialized = serializeAssetWithAnalysis(asset,analysis)
            serializedAssets.append(serialized)
        return (serializedAssets,analysisById)
    def getDroneSnapshot(self)->dict:
        return serializeAutonomousDrone(self.droneController.getSnapshot())
      