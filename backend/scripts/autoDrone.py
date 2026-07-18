from dataclasses import dataclass, replace
from typing import Literal
from datetime import datetime, timezone
from .telemetryGenerator import Asset
from .timeToEntry import AssetAnalysis
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
    def __init__(self, startLong:float, startLat: float, patrolSpeed: float, tolerance: float, interceptSpeed: float, shadowDistance: float):
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
        self.interceptSpeed = interceptSpeed
        self.shadowDistance = shadowDistance
    def getSnapshot(self)->AutonomousDrone:
        return self.drone
    def tick(self,elapsedSeconds: float, patrolPath: dict | None, assets: list[Asset], analysisByAssetId: dict[str, AssetAnalysis])-> AutonomousDrone:
        # Decision priority:
        # 1. Remain idle without an active path
        # 2. Initialize a newly activated path
        # 3. Intercept or shadow a breached asset
        # 4. Otherwise continue patrolling
        
        time = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
        # Without an active patrol path, keep the drone stationary
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
        
        # Restricted-zone targets take priority over normal patrol movement.
        target = self.selectTarget(assets,analysisByAssetId)
        if target is not None:
            isShadowing = self.drone.mode == "shadow" and self.drone.targetId == target.assetId
            if isShadowing:
                return self.shadowTarget(target,elapsedSeconds)
            return self.interceptTarget(target, elapsedSeconds)
            #return self.interceptTarget(target,elapsedSeconds)
        
        targetLongitude, targetLatitude = coordinates[self.currentPathIndex]
        
        newLongitude, newLatitude,heading,_,waypointWasReached = (self.calculateMovement(targetLongitude,targetLatitude,self.patrolSpeed,elapsedSeconds,stoppingDistance=0.0))
        
        if waypointWasReached:
            newLongitude = targetLongitude
            newLatitude = targetLatitude
            self.currentPathIndex = (self.currentPathIndex + 1) % len(coordinates)
            nextLongitude,nextLatitude = coordinates[self.currentPathIndex]
            nextRoute = GEODEISC.Inverse(newLatitude,newLongitude,nextLatitude,nextLongitude    )
            heading = nextRoute["azi1"] % 360
        self.drone = replace(self.drone,longitude=newLongitude, latitude=newLatitude,heading=heading,
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
                             speed=self.patrolSpeed, mode="patrol",targetId=None,
                             sequence=self.drone.sequence+1,timestamp=timestamp)


    def selectTarget(self,assets: list[Asset],analysisById: dict[str,AssetAnalysis])-> Asset | None:
        
        if self.drone.targetId:
            # Check if we are already chasing an asset, if so continue
            for asset in assets:
                if asset.assetId != self.drone.targetId:
                    continue    
                    
                analysis = analysisById.get(asset.assetId)
                if(analysis is not None and analysis.isInsideZone):
                    return asset
                
                
        # Check for new asset to follow
        nearestDistance = float('inf')
        nearestAsset = None
        for asset in assets:
            analysis = analysisById.get(asset.assetId)
            
            if(analysis is None or not analysis.isInsideZone):
                continue
            route = GEODEISC.Inverse(self.drone.latitude,self.drone.longitude, asset.latitude, asset.longitude)
            distance = route["s12"]

            if distance < nearestDistance:
                nearestDistance = distance
                nearestAsset = asset
        return nearestAsset
    def calculateMovement(self, targetLongitude:float, targetLatitude: float, speed:float,
                          elapsedSeconds: float, stoppingDistance: float = 0)->tuple[float,float,float,float,bool]:
        route = GEODEISC.Inverse(
            self.drone.latitude,
            self.drone.longitude,
            targetLatitude,
            targetLongitude
            )

        actualDistance = route["s12"]
        distanceToTarget = max(0.0, actualDistance - stoppingDistance)
        
        heading = route["azi1"] % 360
        # If we are already within shadow distance of target
        if distanceToTarget <= self.tolerance:
            return (self.drone.longitude,self.drone.latitude,heading,actualDistance, True)
        
        currentMovement = min(speed * elapsedSeconds,distanceToTarget)

        destination = GEODEISC.Direct(self.drone.latitude,self.drone.longitude,heading,currentMovement)

        newLat = destination["lat2"]
        newLong = destination["lon2"]
        remainingDistance = distanceToTarget - currentMovement
        reachedStoppingDistance = (remainingDistance <= self.tolerance)
        
        return (newLong,newLat,heading,actualDistance,reachedStoppingDistance)
    def interceptTarget(self, target:Asset,elapsedSeconds:float)->AutonomousDrone:
        newLongitude, newLatitude,heading,_,waypointWasReached = (self.calculateMovement(target.longitude,target.latitude,self.interceptSpeed,elapsedSeconds,stoppingDistance=self.shadowDistance))
        mode: DroneMode = "shadow" if waypointWasReached else "intercept"
        self.drone = replace(self.drone, longitude=newLongitude,latitude=newLatitude,heading=heading,
                             speed=self.interceptSpeed,mode=mode,targetId=target.assetId,
                             sequence = self.drone.sequence +1, timestamp=datetime.now(timezone.utc).isoformat(timespec="milliseconds"))
        return self.drone
    def shadowTarget(self,target:Asset,elapsedSeconds:float)->AutonomousDrone:
        behindHeading = (target.heading +180) % 360
        
        shadowPoint = GEODEISC.Direct(target.latitude,target.longitude,behindHeading,self.shadowDistance)

        shadowLatitude = shadowPoint["lat2"]
        shadowLongitude = shadowPoint["lon2"]

        newLongitude, newLatitude,heading,_, reached = (
            self.calculateMovement(shadowLongitude,shadowLatitude,self.interceptSpeed,
                                   elapsedSeconds,stoppingDistance=0.0 ))
        speed = self.interceptSpeed
        if reached:
            newLongitude = shadowLongitude
            newLatitude = shadowLatitude
            heading = target.heading
            speed = target.speed
        self.drone = replace(self.drone,longitude=newLongitude,latitude=newLatitude,heading=heading,
                            speed=speed,mode="shadow", targetId = target.assetId, sequence=self.drone.sequence+1,
                            timestamp=datetime.now(timezone.utc).isoformat(timespec="milliseconds"))
        return self.drone
            
        
        



