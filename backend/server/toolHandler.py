class ToolHandler:
    def __init__(self):
        self.zonesById = {}
        self.patrolPathsById = {}
        self.activePatrolPathId = None
    # Returns snapshot of toolhandler in processing ready form for frontend 
    def getSnapshot(self):
        return{
            "zones": list(self.zonesById.values()),
            "patrolPaths": list(self.patrolPathsById.values()),
            "activePatrolPathId": self.activePatrolPathId
        }
    # Inserting zone by id
    def insertZone(self, zone: dict):
        self.zonesById[zone.get("id")] = zone
        return zone
    # Removing zone by id
    def removeZone(self, zoneId:dict):
        removed = self.zonesById.pop(zoneId,None)
        return removed
    # Inserting path by id
    def insertPath(self, path:dict):
        self.patrolPathsById[path.get("id")] = path
        return path
     # Removing path by id
    def removePath(self, pathId):
        removed = self.patrolPathsById.pop(pathId,None)
        if self.activePatrolPathId == pathId:
            self.activePatrolPathId = None
        return removed
    # Set active patrol path id
    def setActivePatrolPath(self, pathId: str | None):
        self.activePatrolPathId = pathId
        
        
        
    
