import os
def config()->dict:
        config = {
               "TELEMETRY_SEED":int(os.getenv("TELEMETRY_SEED","100")),
               "TELEMETRY_ASSET_COUNT":int(os.getenv("TELEMETRY_ASSET_COUNT","100")),
               "TELEMETRY_UPDATES_PER_SECOND":int(os.getenv("TELEMETRY_UPDATES_PER_SECOND","2")),
               "FRONTEND_ORIGIN":os.getenv("FRONTEND_ORIGIN","http://localhost:5173"),
               "SERVER_PORT":int(os.getenv("SERVER_PORT","4000")),
               # TODO Update if going to a real ip
                "SERVER_HOST":str(os.getenv("SERVER_HOST","localhost"))
        }
        return config