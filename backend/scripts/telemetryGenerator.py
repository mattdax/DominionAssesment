from .telemetryUtil import generatePositions, generateHeading, generateSpeed, updatePosition
import datetime
from dataclasses import dataclass, replace
from typing import List
import random
from time import monotonic

@dataclass
class Asset:
    assetId: str
    assetType: str
    longitude: float
    latitude: float
    sequence: int
    heading: float
    speed: float 
    timestamp: str


class TelemetryGenerator():
   
   # Initializer for Telemetry Generator
    # Input: see, assetCount, updateFrequency
    def __init__(self, seed:int, assetCount:int, updatesPerSecond:int):
        if updatesPerSecond <= 0:
            raise ValueError("updatesPerSecond must be greater than zero")
        
        self.seed = seed
        self.rnd = random.Random(seed)
        self.assetCount = assetCount
        # Handle 
        self.assets = self._createAssets(assetCount)
        
        self.updatesPerSecond = updatesPerSecond
        
        # Converts the update rate into the expected duration between ticks.
        self.updateIntervalSeconds = 1.0 / updatesPerSecond
        self.maximumElapsedSeconds = self.updateIntervalSeconds * 2
        self.lastElapsedSeconds = 0
        self.running = False
        self.lastTick = monotonic()
    
    # Create assets
    # Input: Assetcount
    def _createAssets(self, assetCount)-> List[Asset]:
        assets = []
        for i in range(assetCount):
            latitude,longitude = generatePositions(self.rnd)
            timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds")
            
            # Create new asset object
            asset = Asset(
            assetId = "drone:"+str(i),
            assetType = "public",
            
            longitude = longitude,
            latitude = latitude,
            # Sequence numbers allow clients to reject info that arrives out of order.
            sequence = 0,
            heading = generateHeading(self.rnd),
            speed = generateSpeed(self.rnd),
            timestamp = timestamp
            
            )
            
            assets.append(asset)
        return assets
    # Updates assets location
    def _updateAssetPosition(self, asset: Asset, elapsedT: float, timestamp:str)-> Asset:
        headingChange = 0
        if self.rnd.random() < 0.1:
            headingChange = self.rnd.uniform(-30.0,30.0)
        if self.rnd.random() < 0.05:
            headingChange = self.rnd.uniform(-90.0,90.0)
        updatedHeading = (asset.heading + headingChange) % 360
        latitude, longitude = updatePosition(asset.latitude, asset.longitude, updatedHeading,asset.speed,elapsedT)
        return replace(asset, latitude=latitude, longitude=longitude, sequence=asset.sequence+1,heading=updatedHeading, timestamp=timestamp)
    
    # 
    def tick(self)->list[Asset]:
        currentTick = monotonic()
        elapsedT = currentTick - self.lastTick
        #elapsedT = max(0.0, elapsedT)
        
        # Limit amount of possible change
        elapsedT = min(elapsedT, self.maximumElapsedSeconds)
        self.lastTick = currentTick
        self.lastElapsedSeconds = elapsedT
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds")
        updatedAssets = []
        # Update positioning for each asset
        for asset in self.assets:
             updatedAssets.append(self._updateAssetPosition(asset,elapsedT=elapsedT, timestamp=timestamp))
        
        # Replace the current snapshot only after every asset has been updated.
        self.assets = updatedAssets
        return updatedAssets
    
    # Resets the generator back to Initial assets
    def reset(self):
        self.lastTick = monotonic()
        self.rnd = random.Random(self.seed)
        self.assets = self._createAssets(self.assetCount)
