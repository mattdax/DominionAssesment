import os
# env config
# TODO: setup .env
def config()->dict:
        config = {
               "TELEMETRY_SEED":int(os.getenv("TELEMETRY_SEED","100")),
               "TELEMETRY_ASSET_COUNT":int(os.getenv("TELEMETRY_ASSET_COUNT","100")),
               "TELEMETRY_UPDATES_PER_SECOND":int(os.getenv("TELEMETRY_UPDATES_PER_SECOND","2")),
               "FRONTEND_ORIGIN":os.getenv("FRONTEND_ORIGIN","http://localhost:5173"),
               "SERVER_PORT":int(os.getenv("SERVER_PORT","4000")),
               # TODO Update if going to a real ip
                "SERVER_HOST":str(os.getenv("SERVER_HOST","localhost")),

                "AUTONOMOUS_DRONE_START_LONGITUDE":float (os.getenv("AUTONOMOUS_DRONE_START_LONGITUDE", "-75.6972")),
                "AUTONOMOUS_DRONE_START_LATITUDE":float (os.getenv("AUTONOMOUS_DRONE_START_LATITUDE", "45.4215")),
                "AUTONOMOUS_DRONE_PATROL_SPEED":float(os.getenv("AUTONOMOUS_DRONE_PATROL_SPEED","100.0")),
                "AUTONOMOUS_DRONE_WAYPOINT_TOLERANCE":float(os.getenv("AUTONOMOUS_DRONE_WAYPOINT_TOLERANCE","5.0"))
        }
        return config