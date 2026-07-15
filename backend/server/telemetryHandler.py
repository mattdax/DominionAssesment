from scripts.telemetryGenerator import TelemetryGenerator
from server.serializer import serializeAsset,serializeAssets

class TelemetryHandler:
    def __init__(self,generator: TelemetryGenerator):
        self.generator = generator
        self.running = False
    
    # Returns current assets
    def getSnapshot(self)-> str:
        return serializeAssets(self.generator.assets)
    
    # Increments assets by tick and returns new assets
    def tick(self)-> str:
        self.generator.tick()
        return serializeAssets(self.generator.assets)
    
    # Returns whether service is active
    def isRunning(self)->bool:
        return self.running
    
    # Sets service to running
    def setRunning(self)->None:
        self.running = not self.running 

     
      