from flask_socketio import SocketIO, emit
from flask import current_app
from .telemetryHandler import TelemetryHandler
from .toolHandler import ToolHandler
socketio = SocketIO()

# Handler fetches
def getTelemetryHandler()->TelemetryHandler:
    return current_app.extensions["telemetry_handler"]
def getToolHandler()->ToolHandler:
    return current_app.extensions["tool_handler"]


@socketio.on("connect")
def connect(auth=None):
    handler = getTelemetryHandler()
    snapshot = handler.getSnapshot()
    # Asset snapshot
    emit("assets.snapshot",{"assets": snapshot})
    toolHandler = getToolHandler()
    # Tool snapshot
    emit("tools.snapshot",toolHandler.getSnapshot())
    
    # Drone Snapshot
    emit("autonomous-drone.snapshot",{"drone": handler.getDroneSnapshot()})


    # Start generation loop
    handler.start()
@socketio.on("zone.insert")
def handleZoneInsert(payload):
    handler = getToolHandler()
    zone = handler.insertZone(payload["zone"])
    socketio.emit("zone.inserted", {"zone":zone})
@socketio.on("path.insert")
def handlePathInsert(payload):
    handler = getToolHandler()
    path = handler.insertPath(payload["path"])
    socketio.emit("path.inserted",{"path":path})
@socketio.on("zone.delete")
def handleZoneDelete(payload):
    handler = getToolHandler()
    handler.removeZone(payload["zoneId"])
    socketio.emit("zone.deleted", {"zoneId": payload["zoneId"]})
@socketio.on("path.delete")
def handlePathDelete(payload):
    handler = getToolHandler()
    handler.removePath(payload["pathId"])
    socketio.emit("path.deleted", {"pathId":payload["pathId"]})
@socketio.on("path.activate")
def handlePathActivate(payload):
    handler = getToolHandler()
    pathId = payload.get("pathId")
    handler.setActivePatrolPath(pathId)
    socketio.emit("path.activated",{"pathId":pathId})