from flask import Flask, jsonify
from flask_cors import CORS
from scripts.telemetryGenerator import TelemetryGenerator
from .telemetryHandler import TelemetryHandler
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

    # Setup Telemetry generator and handler
    generator = TelemetryGenerator(seed=app.config["TELEMETRY_SEED"],assetCount=app.config["TELEMETRY_ASSET_COUNT"],updatesPerSecond=app.config["TELEMETRY_UPDATES_PER_SECOND"])
    telemetryHandler = TelemetryHandler(generator, socketio)
    app.extensions["telemetry_handler"] = telemetryHandler
    
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
    return app