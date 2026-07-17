import { MapLibreMap, type MapLayerMouseEvent, type MapMouseEvent } from "maplibre-gl";
import { useAssetStore } from "../state/useAssetStore";
import { ASSET_LAYER_ID } from "./assetLayer";


export function LoadAssetActions(map:MapLibreMap): ()=>void {
    const removeMapSelection= ()=>{
        useAssetStore.getState().clearSelectedAsset()
    }
    const handleAssetClick = (event: MapLayerMouseEvent) =>{
        const feature = event.features?.[0]
        if(feature?.id === undefined){
            return
        }
        const assetId = String(feature.id)
        useAssetStore.getState().selectAsset(assetId)

    }
    // If map is clicked on, we remove the selected asset, if there is one
    const handleMapClick = (event: MapMouseEvent)=>{
        const clickedAsset = map.queryRenderedFeatures(event.point,{
            layers: [ASSET_LAYER_ID]
        })
        if(clickedAsset.length === 0){
            removeMapSelection()
        }

    }
    map.on("click",ASSET_LAYER_ID,handleAssetClick)
    map.on("click",handleMapClick)
    return() =>{
        map.off("click",ASSET_LAYER_ID, handleAssetClick)
        map.off("click", handleMapClick)
    }
}