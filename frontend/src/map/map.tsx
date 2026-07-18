import { useEffect, useRef, useMemo } from "react"
import { useAssetStore } from "../state/useAssetStore"
import { useAddedToolStore } from "../state/useAddedToolStore"
import { assetsToGeo } from "./assetToGeo"
import maplibregl from "maplibre-gl"
import "maplibre-gl/dist/maplibre-gl.css"
import "./map.css"
import { ASSET_SOURCE_ID, AssetLayer } from "./assetLayer"
import { LoadAssetActions } from "./assetActions"
import { drawControls } from "./drawControls"
import { LoadDrawActions } from "./drawActions"
import { drawToTool } from "./drawToTool"
import type { PatrolPath, RestrictedZone } from "../types/types"
import { socket } from "../realtime/socket"
import { syncToolsToDraw } from "./toolToDraw"
import { DroneLayer, DRONE_SOURCE_ID } from "./droneLayer"
import {
	HistoryLayer,
	PredictionLayer,
	HISTORY_SOURCE_ID,
	PREDICTION_SOURCE_ID
} from "./trajectoryLayers"
import { useDroneStore } from "../state/useDroneStore"
import { droneToGeo } from "./droneToGeo"
import { useAssetTrajectoryQuery } from "../queries/useAssetTrajectoryQuery"
import { historyToGeo, predictionToGeo } from "./trajectoryToGeo"

export function AssetMap() {
	// Setup references
	const container = useRef<HTMLDivElement | null>(null)
	const mapRef = useRef<maplibregl.Map | null>(null)
	const previousSelectedId = useRef<string | null>(null)
	const isApplyingToolSync = useRef(false)

	// Load Store values & functions
	const addPath = useAddedToolStore((state) => state.addPath)
	const addZone = useAddedToolStore((state) => state.addZone)

	const assetsById = useAssetStore((state) => state.assetsById)
	const assetCollection = useMemo(() => assetsToGeo(Object.values(assetsById)), [assetsById])
	const selectedId = useAssetStore((state) => state.selectedAssetId)
	const drone = useDroneStore((state) => state.drone)

	const { data: trajectory } = useAssetTrajectoryQuery(selectedId)

	// Runs on Component Mount
	useEffect(() => {
		let drawControl: ReturnType<typeof drawControls> | undefined
		// if div container does not exist stop
		if (!container.current || mapRef.current) {
			return
		}
		// Init external map actions
		let assetActions: (() => void) | undefined
		let drawActions: (() => void) | undefined
		let toolSync: (() => void) | undefined

		// Define map
		const map = new maplibregl.Map({
			container: container.current,
			style: "https://tiles.openfreemap.org/styles/liberty",
			// Ottawa area
			center: [-75.6972, 45.4215],
			zoom: 9
		})
		// Add Nav Control
		map.addControl(new maplibregl.NavigationControl(), "top-left")

		// Initial Map Setup with assets and layer
		const handleMapLoad = () => {
			const currentAssets = Object.values(useAssetStore.getState().assetsById)
			drawControl = drawControls()

			map.addSource(ASSET_SOURCE_ID, {
				type: "geojson",
				data: assetsToGeo(currentAssets),
				promoteId: "assetId"
			})

			map.addSource(HISTORY_SOURCE_ID, {
				type: "geojson",
				data: historyToGeo(undefined)
			})

			map.addSource(PREDICTION_SOURCE_ID, {
				type: "geojson",
				data: predictionToGeo(undefined)
			})

			map.addLayer(HistoryLayer())
			map.addLayer(PredictionLayer())
			map.addLayer(AssetLayer())
			assetActions = LoadAssetActions(map)
			const drone = useDroneStore.getState().drone
			map.addSource(DRONE_SOURCE_ID, {
				type: "geojson",
				data: drone ? droneToGeo(drone) : { type: "FeatureCollection", features: [] }
			})

			map.addLayer(DroneLayer())

			map.addControl(drawControl)
			drawControl.activate()

			const syncTools = () => {
				isApplyingToolSync.current = true
				try {
					const instance = drawControl?.getTerraDrawInstance()
					if (instance) {
						syncToolsToDraw(instance, useAddedToolStore.getState())
					}
				} finally {
					isApplyingToolSync.current = false
				}
			}

			drawActions = LoadDrawActions(
				drawControl,
				(feature) => {
					if (isApplyingToolSync.current) {
						return
					}
					const tool = drawToTool(feature)
					if (tool.geometry.type == "Polygon") {
						addZone(tool as RestrictedZone)
						socket.emit("zone.insert", { zone: tool as RestrictedZone })
					} else {
						addPath(tool as PatrolPath)
						socket.emit("path.insert", { path: tool as PatrolPath })
						socket.emit("path.activate", { pathId: tool.id })
					}
				},
				(deletedIds) => {
					if (isApplyingToolSync.current) {
						return
					}
					const store = useAddedToolStore.getState()
					for (const id of deletedIds) {
						if (store.zones.some((zone) => zone.id === id)) {
							store.removeZone(id)
							socket.emit("zone.delete", { zoneId: id })
							continue
						}
						if (store.patrolPaths.some((path) => path.id === id)) {
							store.removePath(id)
							socket.emit("path.delete", { pathId: id })
						}
					}
				}
			)
			syncTools()
			toolSync = useAddedToolStore.subscribe(syncTools)
		}
		map.on("load", handleMapLoad)
		mapRef.current = map

		return () => {
			assetActions?.()
			map.off("load", handleMapLoad)
			toolSync?.()
			drawActions?.()
			if (drawControl) {
				map.removeControl(drawControl)
			}
			map.remove()
			mapRef.current = null
		}
	}, [addPath, addZone])

	useEffect(() => {
		const map = mapRef.current
		if (!map) {
			return
		}

		const previousId = previousSelectedId.current
		if (previousId) {
			map.setFeatureState(
				{
					source: ASSET_SOURCE_ID,
					id: previousId
				},
				{
					selected: false
				}
			)
		}
		if (selectedId) {
			map.setFeatureState(
				{
					source: ASSET_SOURCE_ID,
					id: selectedId
				},
				{
					selected: true
				}
			)
		}
		previousSelectedId.current = selectedId
	}, [selectedId])

	// Rerenders on asset updates
	useEffect(() => {
		const map = mapRef.current
		if (!map) {
			return
		}
		const source = map.getSource(ASSET_SOURCE_ID) as maplibregl.GeoJSONSource | undefined
		if (source) {
			source.setData(assetCollection)
		}
	}, [assetCollection])

	useEffect(() => {
		const map = mapRef.current
		if (!map) {
			return
		}
		const source = map.getSource(DRONE_SOURCE_ID) as maplibregl.GeoJSONSource | undefined
		if (source) {
			source.setData(drone ? droneToGeo(drone) : { type: "FeatureCollection", features: [] })
		}
	}, [drone])

	useEffect(() => {
		const map = mapRef.current
		if (!map) {
			return
		}
		const historySource = map.getSource(HISTORY_SOURCE_ID) as maplibregl.GeoJSONSource | undefined
		const predictionSource = map.getSource(PREDICTION_SOURCE_ID) as
			maplibregl.GeoJSONSource | undefined

		const visible = selectedId ? trajectory : undefined
		historySource?.setData(historyToGeo(visible))
		predictionSource?.setData(predictionToGeo(visible))
	}, [trajectory, selectedId])
	return <div ref={container} className="asset-map"></div>
}
