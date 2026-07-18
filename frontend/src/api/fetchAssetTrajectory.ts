import type { AssetTrajectory } from "../types/types"
import { SERVER_HOST, SERVER_PORT } from "../config/config"
import { isAssetTrajectory } from "./assetTrajectoryValidator"

export async function fetchAssetTrajectory(
	assetId: string,
	signal: AbortSignal
): Promise<AssetTrajectory> {
	const response = await fetch(
		"http://" + SERVER_HOST + ":" + SERVER_PORT + "/api/assets/" + assetId + "/trajectory",
		{ signal }
	)
	if (!response.ok) {
		throw new Error("api/fetchAssetTrajectory: Fetch Response not ok")
	}
	const data = await response.json()

	if (isAssetTrajectory(data)) {
		return data
	} else {
		throw new Error("api/fetchAssetTrajectory: Data not parsable to AssetTrajectory")
	}
}
