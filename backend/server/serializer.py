from scripts.telemetryGenerator import Asset
from dataclasses import asdict
from scripts.timeToEntry import AssetAnalysis
from scripts.autoDrone import AutonomousDrone
# Serialize singular asset
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
# Adds analysis to serialized asset.
# TODO Combine serializeAsset and serializeAssetWithAnalysis function
def serializeAssetWithAnalysis(asset:Asset,analysis:AssetAnalysis):
    serializedAsset = serializeAsset(asset)
    serializedAsset["analysis"] = asdict(analysis)
    return serializedAsset

def serializeAutonomousDrone(drone: AutonomousDrone):
    return asdict(drone)

def serializeHistoryAssetPoint(asset: Asset)->dict:
    return{
        "longitude": asset.longitude,
        "latitude": asset.latitude,
        "heading": asset.heading,
        "speed": asset.speed,
        "sequence": asset.sequence,
        "timestamp": asset.timestamp
    }
def serializeAssetTrajectory(assetId: str, history: list[Asset],prediction: dict|None)->dict:
    serializedHistory = []
    for sample in history:
        serializedHistory.append(serializeHistoryAssetPoint(sample))
    return {
        "assetId": assetId,
        "history": serializedHistory,
        "prediction": prediction
    }