from flask import Flask, jsonify
from scripts.telemetryGenerator import TelemetryGenerator
from .telemetryHandler import TelemetryHandler
from .socketHandler import socketio


def create_server()->Flask:
    app = Flask(__name__)
    
    # Setup Telemetry generator and handler
    generator = TelemetryGenerator(100,100,2)
    telemetryHandler = TelemetryHandler(generator, socketio)
    app.extensions["telemetry_handler"] = telemetryHandler
    
    socketio.init_app(app)
    
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