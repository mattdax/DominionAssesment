import type { Asset } from "../types/types";
import { SERVER_HOST, SERVER_PORT } from "../config/config";

type AssetResponse = {
    assets: Asset[]
}

function isRecord(value: unknown): value is Record<string,unknown>{
    return(
        typeof value == "object" && value !== null && !Array.isArray(value)
    )
}
function isAsset(value: unknown): value is Asset{
    if(!isRecord(value)){
        return false
    }

    // Additional checks could be validating ranges of long/lat/heading and timestamp parseable to time    
    return(
        typeof value.assetId == "string" && value.assetId !== null
        && typeof value.assetType == "string" && value.assetType !== null
        && typeof value.longitude == "number" && value.longitude !== null
        && typeof value.latitude == "number" &&  value.latitude !== null
        && typeof value.sequence == "string" && value.sequence !== null
        && typeof value.heading == "number" && value.heading !== null
        && typeof value.speed == "number" &&  value.speed !== null
        && typeof value.timestamp == "string" && value.timestamp !== null
    )
}

function isAssetReponse(value: unknown): value is AssetResponse{
    return (
        isRecord(value) && Array.isArray(value.assets) && value.assets.every(isAsset)
    )
}


export async function fetchAssets(): Promise<Asset[]>{
    const response = await fetch("http://"+SERVER_HOST+":"+SERVER_PORT+"/api/assets")
    if(!response.ok){
        throw new Error("api/fetchAssets: Fetch Response not ok")
    }
    const data = await response.json()

    if(isAssetReponse(data)){
        return data.assets
    }
    else{
        throw new Error("api/fetchAssets: Data not parsable to Asset")
    }
}