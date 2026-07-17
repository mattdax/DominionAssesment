from dataclasses import dataclass
from typing import Literal
from datetime import datetime, timezone

DroneMode = Literal["idle","patrol","intercept","shadow"]

@dataclass
class AutonomousDrone:
    assetId: str
    assetType: str
    longitude: float
    latitude: float
    sequence: int
    heading: float
    speed: float
    timestamp: str
    mode: DroneMode
    targetId: str | None 

class AutonomousDroneController:
    def __init__(self, startLong:float, startLat: float, patrolSpeed: float, tolerance: float):
        time = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
        
        self.drone = AutonomousDrone(assetId="auto:1",
                                    assetType="autonomous",
                                    longitude=startLong,
                                    latitude=startLat,
                                    sequence=0,
                                    heading=0.0,
                                    speed=0.0,
                                    timestamp=time,
                                    mode="idle",
                                    targetId=None)
        self.currentPathIndex = 0
        self.patrolSpeed =patrolSpeed 
        self.tolerance = tolerance
    def getSnapshot(self)->AutonomousDrone:
        return self.drone
