import type { PatrolPath, RestrictedZone } from "../types/types";
import type { FinishedDrawFeature } from "./drawActions";

export function drawToTool(feature: FinishedDrawFeature): RestrictedZone | PatrolPath{
    if(feature.geometry.type=="LineString"){
        return {
            type:"Feature",
            id: String(feature.id),
            geometry: feature.geometry,   
            properties:{
            kind:"patrol-path",
            }

        }
    }
    else{
        return {
            type:"Feature",
            id: String(feature.id),
            geometry: feature.geometry,   
            properties:{
            kind:"restricted-zone",
        }
    }
    }
}
