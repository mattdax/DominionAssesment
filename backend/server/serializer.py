from scripts.telemetryGenerator import Asset
from dataclasses import asdict


def serializeAsset(asset: Asset)-> dict:
    return asdict(asset)

# Serialize a list of assets to JSON string
def serializeAssets(assets: list[Asset])-> list[dict]:
    serializedAssets = []
    for asset in assets:
        serializedAssets.append(
            serializeAsset(asset)
        )
    return serializedAssets


    
