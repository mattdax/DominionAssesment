# Problem 1: Map-based Data Visualization

## Overview
This project is an implementation of Assessment problem 1. It contains a real-time map interface for monitoring 100 simulated assets.

The project contains the functionality to:
- Simulate 100 concurrent realtime assets
- Draw restricted zones and autonomous drone patrol paths
- Calculate the TTE for assets traveling towards restricted zones
- Intercept and shadow assets that have entered restricted zones
- Display 5 minute asset travel history and 5 minute asset travel prediction
- Display details of each asset
- Update events in real time between clients
- Display normal, warning, and critical threat levels

The nearest airport drone deployment extension was not implemented.
## Demo Link
The video demo can be found here: [link](https://youtu.be/iTUvzNJrLsg)

## LLM Usage
### Model
I used ChatGPT 5/Codex as the sole LLM used to assist during development.

### Role In Development
I used the LLM in a collaborative way while building this project. Its main responsibilities were:
- Reviewing incremental code implementations 
- Explaining unfamiliar technical concepts and libraries
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

## Architecture

### Backend Architecture
The backend is built in Python with Flask. It is responsible for telemetry generation, performing any geospatial computations, logging asset history. Backend services are created once and stored in the Flask application. 

The backend acts as the source of information for telemetry, restricted zones, patrol paths, and autonmous drone state. Frontend clients maintain local state for responsive rendering. Shared changes are sent to the backend and broadcast to every connected client.

Application state is stored in memory to keep the assessment focused on real-time simulation and geospatial behaviour. This tradeoff means that the backend state is reset when the server restarts. Persistent storage would be required before running multiple backend instances.

#### Telemetry Generator
Responsible for creating configured assets and updating their position over time using GeographicLib
#### Telemetry Handler
Coordinates simulation updates across the system. It is responsible for advancing asset telemetry, recording assets, calculating the TTE analysis, updating the patrol drone, and broadcasting the resulting updates.

#### ToolHandler
Maintains restricted zones, patrol paths, and the currently active patrol path. 

#### AssetHistory
Responsible for maintining the 5-minute flight history of each asset. Uses a bounded deque to maintain the size of tracked history for each asset and protect against memory growth. 

#### TTE Analysis
Analyzes each asset against the defined restricted zones. Assets and polygons are projected into a metric coordinate system before calculating intersections with Shapely.

An assets heading and speed are used to project a path forward and calculate the nearest zone,if one exists, TTE, and threat level. During the calculation we assume the asset maintains its current heading and speed. The calculation does not use asset history.

I used GeographicLib for asset and drone movement as it calculates headings, distances and destinations from longitude/latitude. I used Shapely for boundary intersection and asset in polygon calculations however a standard x/y plane, not longitude/latitude, so conversion was required. 

#### Trajectory Prediction
Uses at maximum 5 minutes of asset history to calculate average velocity vector over time. Each sample of heading and speed is converted into an x and y velocity vector. Uses GeographicLib to project the resulting vector 5 minutes forward. With this implementation we do not model predicted speed change.

#### Drone Controller
Maintains the state and behaviour of the patrol drone. The controller changes and moves the patrol drone across different modes. Follows the patrol path while there is no asset in a restricted zone, directs to the nearest asset inside of a restricted zone, returns to patrol path upon the asset leaving the restricted zone. Uses GeographicLib to compute the paths to assets and back to patrol paths.

#### Socket Handler

Defines the Socket.IO events used for two way communication between the backend and connected clients. New connections receive snapshots of the current assets, drawing tools, and autonomous drone.

The handler receives restricted-zone and patrol-path commands, updates the shared Tool Handler, and sends the resulting state changes to all clients. Recurring asset and autonomous drone updates are derived by the Telemetry Handler and emitted through the Socket.IO instance.

#### REST API
Endpoints for initial snapshots and predicted/history trajectories.

Trajectory data exists as an endpoint because five-minute history and prediction do not need to be sent for every asset during every telemetry update. 

#### Serializer
Converts backend dataclasses into JSON dictionaries for parsing on the frontend.

### Frontend Architecture
The frontend is built with React and TypeScript using Vite for development. Its capabilities include:
- Receiving initial data and live updates
- Rendering a map and geospatial data using MapLibre
- Adding polygons and lines using TerraDraw
- Selecting assets and presenting their details
- Maintaining client state
- Drawing history and predicted paths
- Changing asset symbology based on threat level
#### Server Data and Validation
TanStack Query handles REST requests and caching. The initial assets snapshot is loaded using a get request. Trajectory data is requested separately once a second. Validator functions verify responses before entering the app state.

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


## Limitations
- While the demo is restricted to the Ottawa area and 100 assets. All properties are changeable for use in different areas and number of assets
- Backend data is only stored in memory and not written to any databases, on server reset the entire state is reset
- The system supports only one autonomous drone and one patrol path.
- TTE does not model acceleration or curved routes
- TTE compares every asset against every zone. This could become computationally demanding in a larger simulation.
 
## Installation

### Prerequisites
The repo requires:

- Python 3.11 or later
- Node.js and npm 

### Backend Setup
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python3 main.py
```
The backend will run at:

```text
http://localhost:4000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The frontend will run at:
```text
http://localhost:5173
```
### Testing

Run the backend tests from the `backend` directory:

```bash
python3 -m unittest discover -s tests -v
```

Run the frontend tests from the `frontend` directory:

```bash
npm test

```

