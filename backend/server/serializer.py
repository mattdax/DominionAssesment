from scripts.telemetryGenerator import Asset
from dataclasses import asdict
from scripts.timeToEntry import AssetAnalysis

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


    
