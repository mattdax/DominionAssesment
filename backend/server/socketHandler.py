from flask_socketio import SocketIO, emit
from flask import current_app
from .telemetryHandler import TelemetryHandler
socketio = SocketIO()

def getTelemetryHandler()->TelemetryHandler:
    return current_app.extensions["telemetry_handler"]

@socketio.on("connect")
def connect(auth=None):
    handler = getTelemetryHandler()
    snapshot = handler.getSnapshot()
    emit("assets.snapshot",{"assets": snapshot})

    handler.start()