import type { Asset } from "../types/types"
import { SERVER_HOST, SERVER_PORT } from "../config/config"
import { isAssetReponse } from "./assetValidator"

export async function fetchAssets(signal: AbortSignal): Promise<Asset[]> {
	const response = await fetch("http://" + SERVER_HOST + ":" + SERVER_PORT + "/api/assets", {
		signal
	})
	if (!response.ok) {
		throw new Error("api/fetchAssets: Fetch Response not ok")
	}
	const data = await response.json()

	if (isAssetReponse(data)) {
		return data.assets
	} else {
		throw new Error("api/fetchAssets: Data not parsable to Asset")
	}
}
