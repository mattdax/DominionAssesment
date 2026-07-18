from math import radians,cos, atan2, hypot, sin, degrees
from scripts.telemetryGenerator import TelemetryGenerator, Asset
from scripts.timeToEntry import returnAnalysis, AssetAnalysis
from scripts.autoDrone import AutonomousDroneController
from scripts.assetHistory import AssetHistory
from server.serializer import serializeAssetWithAnalysis, serializeAutonomousDrone, serializeAssetTrajectory
from flask_socketio import SocketIO
from .toolHandler import ToolHandler
from geographiclib.geodesic import Geodesic

GEODISC = Geodesic.WGS84

class TelemetryHandler:
    def __init__(self,generator: TelemetryGenerator, socketio:SocketIO, 
                 toolHandler: ToolHandler, droneController: AutonomousDroneController,
                 assetHistory: AssetHistory):
        
        self.assetHistory = assetHistory
        self.generator = generator
        self.socketio = socketio
        self.toolHandler = toolHandler
        self.droneController = droneController
        self.running = False
        self.task = None
    
    # Returns current assets
    def getSnapshot(self)-> list[dict]:
        serialized, _ = self.getAnalyzedAssets(self.generator.assets)
        return serialized
    
    # Increments assets by tick and returns new assets
    def tick(self)-> list[dict]:
        updated = self.generator.tick()

        self.assetHistory.recordAssets(updated)

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
        
        # serialize and Set analysis for eash asset
        for asset in assets:
            analysis = returnAnalysis(asset,zones)
            analysisById[asset.assetId] = analysis
            serialized = serializeAssetWithAnalysis(asset,analysis)
            serializedAssets.append(serialized)
        return (serializedAssets,analysisById)
    
    def getDroneSnapshot(self)->dict:
        return serializeAutonomousDrone(self.droneController.getSnapshot())
    
    def getVelocityComponents(self, asset: Asset)-> tuple[float,float]:
        headingRadians = radians(asset.heading)
        xVelocity = asset.speed * sin(headingRadians)
        yVelocity = asset.speed * cos(headingRadians)
        return xVelocity,yVelocity
    def predictPath(self,asset:Asset, predictionSeconds:float = 300):
        history = self.assetHistory.getHistory(assetId=asset.assetId)
        
        if history == []:
            return None
        
        # Right positive, left negative
        totalXVelocity = 0.0
        # Up positive, down negative
        totalYVelocity = 0.0
        for sample in history:
            xVelocity, yVelocity = self.getVelocityComponents(sample)
            totalXVelocity += xVelocity
            totalYVelocity += yVelocity

        
        averageXVelocity = totalXVelocity / len(history)
        averageYVelocity = totalYVelocity / len(history)
        averageSpeed = hypot(averageXVelocity,averageYVelocity)
        averageHeading = (degrees(atan2(averageXVelocity,averageYVelocity))% 360)
        predictionDistance = averageSpeed * predictionSeconds

        predictedEndpoint = GEODISC.Direct(asset.latitude,asset.longitude, averageHeading, predictionDistance)
        return {
            "assetId":asset.assetId,
            "averageHeading": averageHeading,
            "averageSpeed": averageSpeed,
            "predictionSeconds": predictionSeconds,
            "coordinates": [
                [asset.longitude, asset.latitude],
                [predictedEndpoint["lon2"],predictedEndpoint["lat2"]]
            ]   
        }
    def getTrajectory(self, assetId: str)-> dict | None:
        selectedAsset = None

        for asset in self.generator.assets:
            if(asset.assetId == assetId):
                selectedAsset = asset
                break
        if selectedAsset == None:
            return None
        
        history = self.assetHistory.getHistory(assetId)
        prediction = self.predictPath(selectedAsset)

        return serializeAssetTrajectory(
            assetId,
            history,
            prediction
        )
        



        
        
      