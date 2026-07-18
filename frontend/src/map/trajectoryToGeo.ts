import type { FeatureCollection, LineString } from "geojson"

import type { AssetTrajectory } from "../types/types"

type TrajectoryProperties = {
	assetId: string
	kind: "history" | "prediction"
}
function emptyTrajectory(): FeatureCollection<LineString, TrajectoryProperties> {
	return {
		type: "FeatureCollection",
		features: []
	}
}
export function historyToGeo(
	trajectory: AssetTrajectory | null | undefined
): FeatureCollection<LineString, TrajectoryProperties> {
	if (!trajectory) {
		return emptyTrajectory()
	}
	const coords: [number, number][] = trajectory.history.map((point) => [
		point.longitude,
		point.latitude
	])

	return {
		type: "FeatureCollection",
		features: [
			{
				type: "Feature",
				id: "history:" + trajectory.assetId,
				properties: {
					assetId: trajectory.assetId,
					kind: "history"
				},
				geometry: {
					type: "LineString",
					coordinates: coords
				}
			}
		]
	}
}

export function predictionToGeo(
	trajectory: AssetTrajectory | null | undefined
): FeatureCollection<LineString, TrajectoryProperties> {
	if (trajectory === undefined || trajectory === null || trajectory.prediction === null) {
		return emptyTrajectory()
	}

	return {
		type: "FeatureCollection",
		features: [
			{
				type: "Feature",
				id: "prediction:" + trajectory.assetId,
				properties: {
					assetId: trajectory.assetId,
					kind: "prediction"
				},
				geometry: {
					type: "LineString",
					coordinates: trajectory.prediction.coordinates
				}
			}
		]
	}
}
