from dataclasses import dataclass, replace
from typing import Literal
from datetime import datetime, timezone
from geographiclib.geodesic import Geodesic
GEODEISC = Geodesic.WGS84

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
        self.currentPathId: str | None = None
        self.tolerance = tolerance
    def getSnapshot(self)->AutonomousDrone:
        return self.drone
    def tick(self,elapsedSeconds: float, patrolPath: dict | None, assets: list, analysisByAssetId: dict)-> AutonomousDrone:

        time = datetime.now(timezone.utc).isoformat(timespec="milliseconds")

        if(patrolPath == None):
            
            self.currentPathIndex = 0
            self.currentPathId = None
            self.drone = replace(self.drone,mode="idle",speed=0,targetId=None, sequence=self.drone.sequence+1, timestamp=time)
            return self.drone
        parsedPath = self.getPath(patrolPath)
        pathId, coordinates = parsedPath
        
        # check whether the patrol path differs from the currently active path.
        if pathId != self.currentPathId:
            self.activatePath(pathId=pathId,coordinates=coordinates)
            return self.drone
        
        targetLongitude, targetLatitude = (coordinates[self.currentPathIndex])
        
        currentLongitude = self.drone.longitude
        currentLatitude = self.drone.latitude
        # calculates the path from the current drone location to the target waypoint.
        route = GEODEISC.Inverse(currentLatitude,currentLongitude,targetLatitude,targetLongitude)
        distanceToWaypoint = route["s12"]
        headingToWaypoint = route["azi1"] % 360

        travelDistance = (self.patrolSpeed * elapsedSeconds)

        waypointWasReached = (distanceToWaypoint<=self.tolerance or travelDistance >= distanceToWaypoint)
        if(waypointWasReached):
            newLongitude = targetLongitude
            newLatitude = targetLatitude

            self.currentPathIndex = (self.currentPathIndex + 1) % len(coordinates)

            nextLongitude,nextLatitude = (coordinates[self.currentPathIndex])

            nextRoute = GEODEISC.Inverse(newLatitude,newLongitude,nextLatitude,nextLongitude)

            headingToWaypoint = (nextRoute["azi1"] % 360)
        else:
            destination = GEODEISC.Direct(currentLatitude,currentLongitude,headingToWaypoint,travelDistance)
            newLatitude = destination["lat2"]
            newLongitude = destination["lon2"]
        self.drone = replace(self.drone,longitude=newLongitude, latitude=newLatitude,heading=headingToWaypoint,
                             speed=self.patrolSpeed, mode="patrol",targetId=None,sequence=self.drone.sequence+1,timestamp=time)
        return self.drone
        
    
    # Transforms path from dictionary to list of coordiantes
    def getPath(self,patrolPath:dict|None)-> tuple[str, list[tuple[float,float]]] | None:
        pathId = patrolPath.get("id")
        geometry = patrolPath.get("geometry")
        rawCoords = geometry.get("coordinates")

        coordinates: list[tuple[float, float]] = []
        for coorinate in rawCoords:
            long = coorinate[0]
            lat = coorinate[1]
            point =(float(long),float(lat))
            coordinates.append(point)
        if len(coordinates) < 2:
            return None
        return pathId, coordinates
    def activatePath(self,pathId: str, coordinates: list[tuple[float,float]])-> None:
        initialLong, initialLat = coordinates[0]
        nextLong, nextLat = coordinates[1]

        direction = GEODEISC.Inverse(initialLat,initialLong,nextLat,nextLong)
        heading = direction["azi1"] % 360

        timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds")

        self.currentPathId = pathId
        self.currentPathIndex = 1

        self.drone = replace(self.drone,longitude=initialLong, latitude=initialLat, heading=heading, 
                             speed=self.patrolSpeed, mode="patrol",targetId=None,sequence=self.drone.sequence+1,timestamp=timestamp)

        
        return




