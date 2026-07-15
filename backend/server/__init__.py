from flask import Flask, jsonify
from scripts.telemetryGenerator import TelemetryGenerator
from .telemetryHandler import TelemetryHandler
def create_server()->Flask:
    app = Flask(__name__)
    generator = TelemetryGenerator(100,100,2)
    teleHandler = TelemetryHandler(generator)
    @app.get("/health")
    def health():
        return jsonify({
            "status": "online"
        },200)
    return app