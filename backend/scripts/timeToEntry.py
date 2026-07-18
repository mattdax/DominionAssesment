from dataclasses import dataclass
from typing import Any, Literal
from .telemetryGenerator import Asset
from pyproj import Transformer
from shapely.geometry import Point, Polygon, LineString
from math import radians, sin,cos
@dataclass
class AssetAnalysis:
    assetId: str
    isInsideZone: bool
    nearestZoneId: str | None
    distanceToZone: float | None
    entryZoneId: str | None
    tte: float | None
    threatLevel: Literal["normal","warning","critical"]

transformer = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:32618",
    always_xy=True)

# Number of seconds to look ahead with time to entry 
TTE_LOOKAHEAD = 500
# Number of seconds away for high alert
TTE_WARNING = 60

def degreesToMeters(longitude: float,latitude:float)->tuple[float,float]:
    x,y = transformer.transform(longitude,latitude)
    return x,y
# Converts zone to a Polygon type
def zoneToPolygon(zone: dict[str,Any])-> Polygon:
    coords = zone["geometry"]["coordinates"][0]
    convertedCoords = [degreesToMeters(longitude,latitude) for longitude, latitude in coords]
    return Polygon(convertedCoords)

# Calculates the line ahead of an asseet for TTE_LOOKAHEAD   seconds
def projectedPath(asset: Asset, assetPoint: Point)->LineString:
    # degrees to radians
    heading = radians(asset.heading)
    # Total distance traveled over TTE_LOOKAHEAD seconds
    distance = asset.speed * TTE_LOOKAHEAD
    
    # Find dx and dy  
    deltaX = sin(heading) * distance
    deltaY = cos(heading) * distance
    return LineString([(assetPoint.x,assetPoint.y),
                       (assetPoint.x+deltaX, assetPoint.y+deltaY)])


def returnAnalysis(asset: Asset, zones: list[dict[str,Any]])->AssetAnalysis:
    # Shapely treats coordinates as planar units, have to convert the asset into metric units.
    x,y = degreesToMeters(asset.longitude,asset.latitude)
    
    assetPoint = Point(x,y)
    nearestZoneId = None
    nearestDistance = None
    insideZoneId = None
    entryZoneId = None
    earliestTte = None
    threatLevel = "normal"

    projected = (projectedPath(asset,assetPoint))
    # Track the physically nearest zone and earliest predicted entry separately.
    for zone in zones:
        polygon = zoneToPolygon(zone)
        zoneId = str(zone["id"])
        distance = assetPoint.distance(polygon)
        if nearestDistance == None or distance < nearestDistance:
            nearestDistance = distance
            nearestZoneId = zoneId
        # Check if point is inside the polygon
        if polygon.covers(assetPoint):
            if insideZoneId is None:
                insideZoneId = zoneId
            continue
        # Nearest intersection along the projected vector is the entry point.
        projectPolyIntersection = projected.intersection(polygon.boundary)
        if not projectPolyIntersection.is_empty:
            entryDistance = assetPoint.distance(projectPolyIntersection)
            zoneTte = entryDistance / asset.speed
            # Handle path intersecting with multiple zones
            if earliestTte is None or zoneTte < earliestTte:
                earliestTte = zoneTte
                entryZoneId = zoneId
    isInsideZone = insideZoneId is not None
    # If we are inside a zone already set properties correctly
    if isInsideZone:
        entryZoneId = insideZoneId
        earliestTte = 0.0
        threatLevel = "critical"
    elif earliestTte is not None and earliestTte <= TTE_WARNING:
        threatLevel = "warning"
    
    return AssetAnalysis(assetId=asset.assetId,
                         isInsideZone=isInsideZone,
                         nearestZoneId=nearestZoneId,
                         
                         distanceToZone=nearestDistance,
                         entryZoneId=entryZoneId,
                         tte=earliestTte,
                         threatLevel=threatLevel)
