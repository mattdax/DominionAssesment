import type { MaplibreTerradrawControl } from "@watergis/maplibre-gl-terradraw"
import type { GeoJSONStoreFeatures, TerraDrawEventListeners } from "terra-draw"
import type { LineString, Polygon } from "geojson"

export type FinishedDrawFeature = GeoJSONStoreFeatures<LineString> | GeoJSONStoreFeatures<Polygon>

// FinishedDrawFeature validator. Checks proper geometry
function isFinishedDrawFeature(value: GeoJSONStoreFeatures): value is FinishedDrawFeature {
	return value.geometry.type == "Polygon" || value.geometry.type == "LineString"
}

export function LoadDrawActions(
	control: MaplibreTerradrawControl,
	onfinished: (feature: FinishedDrawFeature) => void,
	onDeleted: (featureIds: string[]) => void
): () => void {
	const drawControl = control.getTerraDrawInstance()
	if (!drawControl) {
		throw new Error("LoadDrawActions: Terra Draw instance not found")
	}
	// Finish a drawing action.
	const handleFinish: TerraDrawEventListeners["finish"] = (featureId) => {
		// Verifies correct finish drawing
		const feature = drawControl.getSnapshotFeature(featureId)
		if (!feature || !isFinishedDrawFeature(feature)) {
			return
		}
		onfinished(feature)
	}

	// Handles deletion
	const handleChange: TerraDrawEventListeners["change"] = (featureIds, changeType) => {
		if (changeType == "delete") {
			onDeleted(featureIds.map(String))
		}
	}

	drawControl.on("finish", handleFinish)
	drawControl.on("change", handleChange)
	return () => {
		drawControl.off("finish", handleFinish)
		drawControl.off("change", handleChange)
	}
}
