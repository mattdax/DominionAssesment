import type { Asset } from "../types/types"

export type AssetResponse = {
    assets: Asset[]
}

export function isRecord(value: unknown): value is Record<string,unknown>{
    return(
        typeof value == "object" && value !== null && !Array.isArray(value)
    )
}
export function isAsset(value: unknown): value is Asset{
    if(!isRecord(value)){
        return false
    }

    // Additional checks could be validating ranges of long/lat/heading and timestamp parseable to time    
    return(
        typeof value.assetId == "string" && value.assetId !== null
        && typeof value.assetType == "string" && value.assetType !== null
        && typeof value.longitude == "number" && value.longitude !== null
        && typeof value.latitude == "number" &&  value.latitude !== null
        && typeof value.sequence == "number" && value.sequence !== null
        && typeof value.heading == "number" && value.heading !== null
        && typeof value.speed == "number" &&  value.speed !== null
        && typeof value.timestamp == "string" && value.timestamp !== null
    )
}

export function isAssetReponse(value: unknown): value is AssetResponse{
    return (
        isRecord(value) && Array.isArray(value.assets) && value.assets.every(isAsset)
    )
}