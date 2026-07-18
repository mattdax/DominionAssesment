# Problem 1: Map-based Data Visualization

## Overview
This project is an implementaion of Assessment problem 1. It contains a real-time map interface for monitoring 100 simulated assets.

The map contains the functionality to:
- Draw restricted zones and autonomous drone patrol paths
- Calculate the Time To Entry for assets traveling towards restricted zones
- Intercept and Shadow assets that have entered restricted zones
- Display 5 minute asset travel history and 5 minute asset travel prediction
- Display details of each asset
- Update events in real time between clients 

## Demo Link
The video demo can be found here: INSERT LINK

## Architecture

### Backend Architecture
The backend is built in Python with Flask. It is responsible for telemetry generation, performing any geospatial computations, logging asset history, and maintaining synchronization across connected clients. 
#### Telemetry Generator
Responsible for creating configured assets and updating their position over time using GeographicLib
#### Telemetry Handler
Coordinates simulation updates across the system. It is responsible for advancing asset telemetry, recording assets, calculating the TTE analysis, updating the patrol drone, and broadcasts said updates through socket.io.

#### ToolHandler
Maintains restricted zones, patrol paths, and the currently active patrol path.

#### AssetHistory
Responsible for maintining the 5-minute flight history of each asset. Uses a deque to maintin the size of tracked history for each asset. 

#### TTE Analysis
Analyzes each asset agains the defined restricted zones. Assets and polygons are projected into a metric coordinate system before calculating intersections with Shapely. An assets heading and spped are used to project a path forwards and calculated the nearest zone(if there is), TTE, and threat level.

#### Drone Controller
Maintains the state and behaviour of the patrol drone. The controller changes and moves the patrol drone across differ modes. Follows the patrol path while there is no asset in a restricted zone, directs to the nearest asset inside of a restricted zone, returns to patrol path upon the asset leaving the restricted zone. Uses GeographicLib to comput the paths to assets and back to patrol paths. 

#### Socket Handler
Defines the socket.io to communicate between the backend and connected clients. New connections receive current snapshots of assets, drawed tools, and the autonomous drone. It also consistently updates assets, TTE anaylsis, tools, and drones in real time. 

#### REST API
Endpoints for initial snapshots, and predicted/history trajectories. Used for trajectories as they do not need to be loaded for every asset on the map in real time. 


### Component Responsibilities
### Data Flow
### Source of Truth and Client Synchronization

## Domain Design
### Data Models
### Telemetry Pipeline
### Restricted Zones and TTE
### Predicted Trajectories
### Drone State Machine

## Architectural Decisions and Tradeoffs
## Performance Considerations
## Failure Handling and Assumptions
## Testing
## Known Limitations
## What I Would Build Next
## LLM Usage