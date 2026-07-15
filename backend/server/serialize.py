from scripts.telemetryGenerator import Asset
from dataclasses import asdict
import json

def serializeAsset(asset: Asset)-> str:
    return json.dumps(asdict(asset))

# Serialize a list of assets to JSON string
def serializeAssets(assets: list[Asset])-> str:
    serializedAssets = []
    for asset in assets:
        serializedAssets.append(
            asdict(asset)
        )
    return json.dumps(serializedAssets)


    
