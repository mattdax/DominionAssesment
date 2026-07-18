import { useEffect } from 'react'
import { AssetDetails } from './map/assetDetails'
import './App.css'
import { useAssetQuery } from './queries/useAssetQuery'
import { useAssetStore } from './state/useAssetStore'
import { useSocket } from './realtime/useSocket'
import { AssetMap } from './map/map'
function App() {
	const { data: assets, isPending, isError, error } = useAssetQuery()
	const setAssets = useAssetStore((state) => state.setAssets)
	// for testing
	const storedAssetCount = useAssetStore((state) => Object.keys(state.assetsById).length)

	useEffect(() => {
		if (assets) {
			setAssets(assets)
		}
	}, [assets, setAssets])

	useSocket(true)

	const connectionStatus = isError ? 'Offline' : isPending ? 'Connecting' : 'Online'
	return (
		<div className="app">
			<header className="app-header">
				<p className="app-label">Live Asset Monitoring</p>

				<div className="app-status">
					<span>{connectionStatus}</span>
					<span>{storedAssetCount} assets</span>
				</div>
			</header>
			<main className="app-main">
				{isError ? (
					<div className="app-error">
						<h2>Telemetry currently unavailable</h2>
						<p>{error.message}</p>
					</div>
				) : isPending ? (
					<div className="app-error">
						<p>Loading live telemetry…</p>
					</div>
				) : (
					<>
						<AssetMap />
						<AssetDetails />
					</>
				)}
			</main>
		</div>
	)
}

export default App
