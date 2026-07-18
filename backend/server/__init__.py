from flask import Flask, jsonify
from flask_cors import CORS

from scripts.telemetryGenerator import TelemetryGenerator
from scripts.assetHistory import AssetHistory
from scripts.autoDrone import AutonomousDroneController
from .telemetryHandler import TelemetryHandler
from.toolHandler import ToolHandler
from .socketHandler import socketio
from .config import config


def create_server()->Flask:
    app = Flask(__name__)
    
    # Set Config
    app.config.from_mapping(config())

    # Config CORS
    CORS(app, resources={
        "/api/*":{
            "origins":[
                app.config["FRONTEND_ORIGIN"]
            ],
            "methods":[
                "GET","OPTIONS"
            ]
        }
    }
    )

    # Setup Telemetry generator+handler, Tool handler, and Drone controller
    droneController = AutonomousDroneController(startLong=app.config["AUTONOMOUS_DRONE_START_LONGITUDE"], startLat=app.config["AUTONOMOUS_DRONE_START_LATITUDE"],
                                                patrolSpeed=app.config["AUTONOMOUS_DRONE_PATROL_SPEED"],tolerance=app.config["AUTONOMOUS_DRONE_WAYPOINT_TOLERANCE"], 
                                                interceptSpeed=app.config["AUTONOMOUS_DRONE_INTERCEPT_SPEED"], shadowDistance=app.config["AUTONOMOUS_DRONE_SHADOW_DISTANCE"])
    app.extensions["drone_controller"] = droneController
    
    toolHandler = ToolHandler()
    app.extensions["tool_handler"] = toolHandler
   
    

    generator = TelemetryGenerator(seed=app.config["TELEMETRY_SEED"],assetCount=app.config["TELEMETRY_ASSET_COUNT"],updatesPerSecond=app.config["TELEMETRY_UPDATES_PER_SECOND"])
    
    assetHistory = AssetHistory(historySeconds=app.config["ASSET_HISTORY_SECONDS"],updatesPerSecond=app.config["TELEMETRY_UPDATES_PER_SECOND"])
    assetHistory.recordAssets(generator.assets)
    app.extensions["asset_history"] = assetHistory
    
    telemetryHandler = TelemetryHandler(generator, socketio, toolHandler, droneController,assetHistory)
    app.extensions["telemetry_handler"] = telemetryHandler
    

    # Setup toolHandler
    

    socketio.init_app(app,cors_allowed_origins=[app.config["FRONTEND_ORIGIN"],])
    
    @app.get("/health")
    def health():
        return jsonify({
            "status": "online"
        }),200
    
    @app.get("/api/assets")
    def getAssets():
        return jsonify({
            "assets": telemetryHandler.getSnapshot()
        })
    @app.get("/api/assets/<assetId>/trajectory")
    def getTrajectory(assetId: str):
        trajectory = telemetryHandler.getTrajectory(assetId)
        if trajectory == None:
            return jsonify({
                "error": "Error with generting trajectory"
            }),404
        return jsonify(trajectory),200
    return app