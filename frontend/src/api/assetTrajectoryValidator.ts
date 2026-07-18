import type { AssetHistoryPoint, AssetPrediction, AssetTrajectory } from "../types/types"
import { isRecord } from "./assetValidator"

function isFiniteNumber(value: unknown): value is number {
	return typeof value === "number" && Number.isFinite(value)
}

function isCoordinate(value: unknown): value is [number, number] {
	return (
		Array.isArray(value) &&
		value.length === 2 &&
		isFiniteNumber(value[0]) &&
		isFiniteNumber(value[1])
	)
}

export function isAssetHistoryPoint(value: unknown): value is AssetHistoryPoint {
	if (!isRecord(value)) {
		return false
	}

	return (
		isFiniteNumber(value.longitude) &&
		isFiniteNumber(value.latitude) &&
		isFiniteNumber(value.heading) &&
		isFiniteNumber(value.speed) &&
		isFiniteNumber(value.sequence) &&
		typeof value.timestamp === "string"
	)
}

export function isAssetPrediction(value: unknown): value is AssetPrediction {
	if (!isRecord(value)) {
		return false
	}

	return (
		typeof value.assetId === "string" &&
		isFiniteNumber(value.averageHeading) &&
		isFiniteNumber(value.averageSpeed) &&
		isFiniteNumber(value.predictionSeconds) &&
		Array.isArray(value.coordinates) &&
		value.coordinates.every(isCoordinate)
	)
}

export function isAssetTrajectory(value: unknown): value is AssetTrajectory {
	if (!isRecord(value)) {
		return false
	}

	return (
		typeof value.assetId === "string" &&
		Array.isArray(value.history) &&
		value.history.every(isAssetHistoryPoint) &&
		(value.prediction === null || isAssetPrediction(value.prediction))
	)
}
