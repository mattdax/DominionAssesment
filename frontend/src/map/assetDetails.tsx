import { useAssetStore } from "../state/useAssetStore"

export function AssetDetails() {
	const selectedAsset = useAssetStore((state) => {
		if (!state.selectedAssetId) {
			return undefined
		}
		return state.assetsById[state.selectedAssetId]
	})
	if (!selectedAsset) {
		return undefined
	}
	const { analysis } = selectedAsset
	return (
		<aside className="asset-details">
			<h2>{selectedAsset.assetId}</h2>
			<p>Threat: {analysis.threatLevel}</p>
			<p>
				TTE: {analysis.tte === null ? "No predicted entry" : `${Math.floor(analysis.tte)} seconds`}
			</p>
			<p>
				Distance:{" "}
				{analysis.distanceToZone === null
					? "No restricted zones"
					: `${Math.round(analysis.distanceToZone)} metres`}
			</p>
			<p>Speed: {selectedAsset.speed.toFixed(1)} m/s</p>
		</aside>
	)
}
