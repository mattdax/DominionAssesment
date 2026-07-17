import type { GeoJSONStoreFeatures,TerraDraw } from "terra-draw"
import type { AddedTool,PatrolPath,RestrictedZone } from "../types/types"

type Tool = PatrolPath | RestrictedZone

function toolToTerraFeature(tool: Tool): GeoJSONStoreFeatures{
    const properties: Record<string,string> ={
        kind: tool.properties.kind,
        mode: tool.geometry.type === "Polygon" ? "polygon": "linestring"
    }
    if(tool.properties.name != undefined){
        properties.name=tool.properties.name
    }
    return {
        type:"Feature",
        id: tool.id,
        geometry: tool.geometry,
        properties
    }
}

export function syncToolsToDraw(draw: TerraDraw, state: AddedTool): void {
    const tools: Tool[] = [...state.zones,...state.patrolPaths]
    // Get all tool ids
    const ids = new Set(tools.map((tool)=>tool.id))
    for (const tool of tools){
        const feature = toolToTerraFeature(tool)
        // If tool does not exist yet
        if(!draw.hasFeature(tool.id)){
            draw.addFeatures([feature])
            continue
        }
        // If tool already exists
        const currentTool = draw.getSnapshotFeature(tool.id)
        if(!currentTool){
            continue
        }
        // Update existing tools geometry
        const geoChanged = JSON.stringify(currentTool.geometry) !== JSON.stringify(tool.geometry)
        if(geoChanged){
            draw.updateFeatureGeometry(tool.id, tool.geometry)
        }
        const propsChanged = tool.properties.kind !== currentTool.properties.kind || tool.properties.name !== currentTool.properties.name

        if(propsChanged){
            draw.updateFeatureProperties(tool.id, {
                kind: tool.properties.kind,
                name: tool.properties.name
            })
        }
    }
    const currentToolFeatures = draw.getSnapshot().filter((feature)=>{
        return (feature.properties.kind === "restricted-zone" || feature.properties.kind === "patrol-path")
    })
    for(const feature of currentToolFeatures){
        if(feature.id !== undefined && !ids.has(String(feature.id))){
            draw.removeFeatures([feature.id])
        }
    }
}
