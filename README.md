# Problem 1: Map-based Data Visualization

## Overview
This project is an implementation of Assessment problem 1. It contains a real-time map interface for monitoring 100 simulated assets.

The map contains the functionality to:
- Draw restricted zones and autonomous drone patrol paths
- Calculate the Time To Entry for assets traveling towards restricted zones
- Intercept and Shadow assets that have entered restricted zones
- Display 5 minute asset travel history and 5 minute asset travel prediction
- Display details of each asset
- Update events in real time between clients 

The only missing feature is the airport and drone spawning functionality, with remaining time I prioritized quality.
## Demo Link
The video demo can be found here: INSERT LINK

## Architecture

### Backend Architecture
The backend is built in Python with Flask. It is responsible for telemetry generation, performing any geospatial computations, logging asset history. Backend services are created once and stored in the Flask application. 

The backend acts as the source of information in order to maintain synchronization across connected clients. However, data is stored in memory and not to a database. 

#### Telemetry Generator
Responsible for creating configured assets and updating their position over time using GeographicLib
#### Telemetry Handler
Coordinates simulation updates across the system. It is responsible for advancing asset telemetry, recording assets, calculating the TTE analysis, updating the patrol drone, and broadcasts said updates through socket.io.

#### ToolHandler
Maintains restricted zones, patrol paths, and the currently active patrol path. 

#### AssetHistory
Responsible for maintining the 5-minute flight history of each asset. Uses a bounded deque to maintain the size of tracked history for each asset and protect against memory growth. 

#### TTE Analysis
Analyzes each asset against the defined restricted zones. Assets and polygons are projected into a metric coordinate system before calculating intersections with Shapely.

An assets heading and spped are used to project a path forwards and calculated the nearest zone(if there is), TTE, and threat level. During the calculation we assume the asset maintins the current heading, does not use asset history.

#### Trajectory Prediction
Uses at maximum 5 minutes of asset history to calculate average velocity vector over time. Each sample of heading and speed is converted into an x and y velocity vector. Uses GeographicLib to project the resulting vector 5 minutes forward. With this implementation we do not model predicted speed change.

#### Drone Controller
Maintains the state and behaviour of the patrol drone. The controller changes and moves the patrol drone across different modes. Follows the patrol path while there is no asset in a restricted zone, directs to the nearest asset inside of a restricted zone, returns to patrol path upon the asset leaving the restricted zone. Uses GeographicLib to compute the paths to assets and back to patrol paths.

#### Socket Handler

Defines the Socket.IO events used for both way communication between the backend and connected clients. New connections receive snapshots of the current assets, drawing tools, and autonomous drone.

The handler receives restricted-zone and patrol-path commands, updates the shared Tool Handler, and sends the resulting state changes to all clients. Recurring asset and autonomous drone updates are derived by the Telemetry Handler and emitted through the Socket.IO instance.

#### REST API
Endpoints for initial snapshots, and predicted/history trajectories. 

Trajectory data exists as an endpoint because five-minute history and prediction do not need to be sent for every asset during every telemetry update. 

#### Serializer
Converts backend dataclasses into JSON dictionaries for parsing on the frontend.

### Backend Data Flow
General Flow of data Telemetry Generator -> Telemetry Handler -> History/TTE/Prediction -> Serializer -> Socket.IO / Rest API -> Clients

### Frontend Architecture
The frontend is built with React and TypeScript using Vite for development. Its capabilities include:
- Receiving initial data and live updates
- Rendering a map and geospatial data using MapLibre
- Adding polygons and lines using TerraDraw
- Selecting assets and present details
- Maintaining client state
- Drawing history and predicted paths
- Changing asset symbology based on distance to zone
#### Server Data and Validation
TanStack query handles REST requests and caching. The initial assets snapshot is loaded using a get method. Trajectory data is requested seperately once a second. Validator functions verify responses before entering the app state.

#### Realtime Synchronization
A single shared Socket.IO client receives asset telemetry, restricted zones, patrol paths, path activation, and autonomous drone state.

Incremental asset updates are accepted only when their sequence number is greater than the most recent sequence number. Zone and path updates use their IDs to replace existing geometry rather than creating duplicates.

#### Client State
The frontend uses 3 Zustand stores.
- The asset store maintains assets indexed by ID 
- The tool store maintains zones and paths
- The drone store maintains the autonomous drone state
#### Map Rendering
MapLibre is responsible for rendering assets, historical/predicted trajectories, and the autonomous drone. These data types are converted into GeoJSON and maintained through their own sources and layers. 

Restricted zones and patrol paths are rendered and edited through Terra Draw, which maintains its own internal geometry store.

## Domain Design
### Data Models
### Telemetry Pipeline
### Restricted Zones and TTE
### Predicted Trajectories

## Architectural Decisions and Tradeoffs
## Performance Considerations
## Failure Handling and Assumptions
## Testing

## Limitations
- While the demo is restricted to the Ottawa area and 100 assets. All properties are changeable for use in different areas and number of assets
- Backend data is only stored in memory and not written to any databases, on server reset the entire state is reset
- The system supports only one autonomous drone and one patrol path.
- TTE does not model acceleration or curved routes
- TTE compares every asset against every zone, in a larger simulation, this could become compuationally demanding.
## LLM Usage
### Model
I used ChatGPT 5/Codex as the sole LLM for aid during the development of this project.

### Role In Development
I used the LLM in an collabrative way while building this project. Its main responsibilities were:
- Reviewing incremental code implementations 
- Explaining unfamiliar topics including or libraries
- Diagnosing errors, test failures, stale query data, and client synchronization issues
- Suggesting backend and frontend test cases and generating test data
I did not use an LLM to generate an entire project or have it directly add any functionality.

### Specifications Provided
- The current development goal, such as calculating TTE, synchronizing clients, or implementing autonomous drone movement
- Runtime errors, stack traces, TypeScript errors, and failing test output
- General current goal (ie; method for calculating TTE, what GeographicLib functions to use, etc)
- Relevant functions or data models

### Workflow and Prompting
The LLM was used as an iterative pair-programming and review tool. Development was divided into small features, with the current implementation reviewed after each milestone.

I typically provided the current objective, relevant implementation context, and any errors or unexpected behavior. I then reviewed the response before implementing the solution myself or requesting a narrowly scoped change.

Examples included selecting appropriate GeographicLib operations, diagnosing Socket.IO synchronization behavior, explaining TTE calculations, and suggesting unit tests. 


