import type { Point, Feature, FeatureCollection } from "geojson";
import type { Asset } from "../types/types";

type AssetProperties ={
    assetId: string,
    assetType: string,
    heading:number,
    speed:number,
    sequence:number,
    timestamp:string
}

export function assetToGeo(asset: Asset): Feature<Point,AssetProperties> {
    
    return {
        type: "Feature",
        properties:{
            assetId: asset.assetId,
            assetType:asset.assetType,
            heading:asset.heading,
            speed:asset.speed,
            sequence:asset.sequence,
            timestamp: asset.timestamp
        },
        geometry: {
            type:"Point",
            coordinates: [asset.longitude,asset.latitude]
        }

    }
}

export function assetsToGeo(assets: Asset[]): FeatureCollection<Point> {
    const mappedFeatures = assets.map(assetToGeo)
    const collection: FeatureCollection<Point> = {

        type: "FeatureCollection",
        features: mappedFeatures
    }
    return collection
}
   