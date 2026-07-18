import { useAssetStore } from '../state/useAssetStore'

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
	const timeToEntry =
		analysis.tte === null ? 'No Zone Entry Ahead' : `${Math.floor(analysis.tte)} s`
	const distanceToZone =
		analysis.distanceToZone === null
			? 'No restricted zones'
			: `${Math.round(analysis.distanceToZone)} m`
	return (
		<aside className="asset-details">
			<header className="asset-details-header">
				<p className="asset-details-label">Asset ID</p>
				<h2>{selectedAsset.assetId}</h2>
				<span className={`asset-details-threat asset-details-${analysis.threatLevel}`}>
					{analysis.threatLevel}
				</span>
			</header>

			<dl className="asset-details-metrics">
				<div>
					<dt>Time to entry</dt>
					<dd>{timeToEntry}</dd>
				</div>

				<div>
					<dt>Distance to nearest zone</dt>
					<dd>{distanceToZone}</dd>
				</div>

				<div>
					<dt>Speed</dt>
					<dd>{selectedAsset.speed.toFixed(1)} m/s</dd>
				</div>

				<div>
					<dt>Heading</dt>
					<dd>{Math.round(selectedAsset.heading)}°</dd>
				</div>
			</dl>
		</aside>
	)
}
