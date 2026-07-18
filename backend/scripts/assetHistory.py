from .telemetryGenerator import Asset
from collections import deque

class AssetHistory:
    def __init__(self,historySeconds,updatesPerSecond):
        # Should be 600
        self.maximumSamples = historySeconds * updatesPerSecond

        self.historyByAssetId: dict [ str, deque[Asset]] = {}
    def recordAssets(self, assets:list[Asset])-> None:
        for asset in assets:
            history = self.historyByAssetId.get(asset.assetId)
            # If no history for an asset exists, create deque
            if history is None: 
                history = deque(maxlen=self.maximumSamples)
                self.historyByAssetId[asset.assetId] = history
            if history and history[-1].sequence >= asset.sequence:
                continue
            history.append(asset)
    def getHistory(self,assetId:str)-> list[Asset]:
        history = self.historyByAssetId.get(assetId)
        if not history:
            return []
        return list(history)
    def clear(self)->None:
        self.historyByAssetId.clear()