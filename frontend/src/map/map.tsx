import { useEffect, useRef, useMemo } from "react"
import { useAssetStore } from "../state/useAssetStore"
import { useAddedToolStore } from "../state/useAddedToolStore"
import { assetsToGeo } from "./assetToGeo"
import maplibregl from "maplibre-gl"
import "maplibre-gl/dist/maplibre-gl.css"
import "./map.css"
import { ASSET_SOURCE_ID, AssetLayer } from "./assetLayer"
import { LoadAssetActions } from "./assetActions"
import { drawControls } from "./drawControls"
import { LoadDrawActions } from "./drawActions"
import { drawToTool } from "./drawToTool"
import type { PatrolPath, RestrictedZone } from "../types/types"




export function AssetMap(){
    // Setup references
    const container = useRef<HTMLDivElement | null>(null)
    const mapRef = useRef<maplibregl.Map | null> (null)
    const previousSelectedId = useRef<string | null>(null);
    
    // Load Stores
    const addPath = useAddedToolStore((state)=> state.addPath)
    const addZone = useAddedToolStore((state)=> state.addZone)
    
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
        // Init external map actions
        let assetActions: (() => void) | undefined;
        let drawActions: (()=> void) | undefined

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

            drawActions = LoadDrawActions(drawControl,(feature)=>{
                const tool = drawToTool(feature);
                if(tool.geometry.type == "Polygon"){
                    addZone(tool as RestrictedZone)
                }
                else{
                     addPath(tool as PatrolPath)
                }
            },
            (deletedIds)=>{
                const store = useAddedToolStore.getState()
                for(const id of deletedIds){
                    if(store.zones.map((zone)=>zone.id == id)){
                        store.removeZone(id)
                        continue
                    }
                    if(store.patrolPaths.map((path)=>path.id == id)){
                        store.removePath(id)
                    }
                }
            }
        )

        }
        map.on("load",handleMapLoad)
        mapRef.current = map
        
        return ()=>{
            assetActions?.()
            map.off("load",handleMapLoad)
            drawActions?.();
            if(drawControl){
                map.removeControl(drawControl)
            }
            map.remove()
            mapRef.current = null
        }
    },[addPath,addZone])

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