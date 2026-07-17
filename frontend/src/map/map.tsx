import { useEffect, useRef, useMemo } from "react"
import { useAssetStore } from "../state/useAssetStore"
import { assetsToGeo } from "./assetToGeo"
import maplibregl from "maplibre-gl"
import "maplibre-gl/dist/maplibre-gl.css"
import "./map.css"
import { ASSET_SOURCE_ID, AssetLayer } from "./assetLayer"
import { LoadAssetActions } from "./assetActions"
import { drawControls } from "./drawControls"





export function AssetMap(){
    const container = useRef<HTMLDivElement | null>(null)
    const mapRef = useRef<maplibregl.Map | null> (null)
    const previousSelectedId = useRef<string | null>(null);
    
    
    const assetsById = useAssetStore((state)=> state.assetsById)
    const assetCollection = useMemo(()=> assetsToGeo(Object.values(assetsById)),[assetsById])
    const selectedId = useAssetStore((state)=>state.selectedAssetId)

    
    // Runs on Component Mount
    useEffect(()=>{
       let drawControl: ReturnType<typeof drawControls> | undefined
        // if div container does not exist stop
        if(!container.current || mapRef.current){
            return
        }

        let assetActions: (() => void) | undefined;

        // Define map
        const map = new maplibregl.Map({container: container.current, 
                    style: "https://tiles.openfreemap.org/styles/liberty",
                    // Ottawa area
                    center: [-75.6972, 45.4215],
                    zoom: 9    
                })
        map.addControl(new maplibregl.NavigationControl(),"top-left")
        
       
        // Initial Map Setup with assets and layer
        const handleMapLoad = ()=>{
            const currentAssets = Object.values(useAssetStore.getState().assetsById)
            drawControl = drawControls()
            
            map.addSource(ASSET_SOURCE_ID, {
                type:"geojson",
                data:assetsToGeo(currentAssets),
                promoteId:"assetId"
            })
            map.addLayer(AssetLayer())
            assetActions = LoadAssetActions(map)
            map.addControl(drawControl)

        }
        map.on("load",handleMapLoad)
        mapRef.current = map
        
        return ()=>{
            assetActions?.()
            map.off("load",handleMapLoad)
            if(drawControl){
                map.removeControl(drawControl)
            }
            map.remove()
            mapRef.current = null
        }
    },[])

    useEffect(()=>{
        const map = mapRef.current
        if(!map){
            return
        }
        const previousId = previousSelectedId.current
        if(previousId){
             map.setFeatureState({
                source: ASSET_SOURCE_ID,
                id: previousId
            },{
                selected: false
            })
        }
        if(selectedId){
            map.setFeatureState({
                source: ASSET_SOURCE_ID,
                id: selectedId
            },{
                selected: true
            })
        }
        previousSelectedId.current = selectedId
    },[selectedId])

    // Rerenders on asset updates
    useEffect(()=>{
        const map = mapRef.current
        if (!map){
            return
        }
        const source= map.getSource(ASSET_SOURCE_ID) as maplibregl.GeoJSONSource | undefined
        if(source){
            source.setData(assetCollection)
        }
    },[assetCollection])
    return (<div ref={container} className="asset-map"></div>)
}