from random import Random
from geographiclib.geodesic import Geodesic


# Define area assets can generate in
MAX_LAT = 45.50
MIN_LAT = 45.30

MAX_LONG = -75.55
MIN_LONG = -75.90

# Define min and max speeds in M/s
# .1 km per minute slowest
# 2 km per minute fastest

MIN_SPEED = 1.666
MAX_SPEED = 66.666

# Geo setup
GEODISC = Geodesic.WGS84

# Generates initial positions for assets
def generatePositions(seed: Random) -> tuple[float,float]:
    latitude = seed.uniform(MIN_LAT,MAX_LAT)
    longitude = seed.uniform(MIN_LONG,MAX_LONG)
    return latitude,longitude

# Generates initial speed for assets
def generateSpeed(seed: Random) -> float:
    return seed.uniform(MIN_SPEED,MAX_SPEED)

# Generate initial heading for assets
def generateHeading(seed: Random)->float:
    return seed.uniform(0,360)

# Updates asset position
def updatePosition(latitude:float, longitude:float, heading:float, speed:float, elapsedT: float)-> tuple[float,float]:
    # Calc traveled distance
    distance = speed * elapsedT
    
    destination = GEODISC.Direct(latitude,longitude,heading,distance)
    return destination["lat2"], destination["lon2"]