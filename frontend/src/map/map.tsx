import { useEffect, useRef, useMemo } from "react"
import { useAssetStore } from "../state/useAssetStore"
import { assetsToGeo } from "./assetToGeo"
import maplibregl from "maplibre-gl"
import "maplibre-gl/dist/maplibre-gl.css"
import "./map.css"


const ASSET_SOURCE_ID = "public-assets";
const ASSET_LAYER_ID = "public-assets-icons";



export function AssetMap(){
    const container = useRef<HTMLDivElement | null>(null)
    const mapRef = useRef<maplibregl.Map | null> (null)
    
    const assetsById = useAssetStore((state)=> state.assetsById)

    const assetCollection = useMemo(()=> assetsToGeo(Object.values(assetsById)),[assetsById])

    useEffect(()=>{
        // if div container does not exist stop
        if(!container.current || mapRef.current){
            return
        }


        // Define map
        const map = new maplibregl.Map({container: container.current, 
                    style: "https://tiles.openfreemap.org/styles/liberty",
                    // Ottawa area
                    center: [-75.6972, 45.4215],
                    zoom: 9    
                })
        map.addControl(new maplibregl.NavigationControl(),"top-left")
        
        // Initial Map Setup with assets
        const handleMapLoad = ()=>{
            const currentAssets = Object.values(useAssetStore.getState().assetsById)
            map.addSource(ASSET_SOURCE_ID, {
                type:"geojson",
                data:assetsToGeo(currentAssets)
            })
            map.addLayer({
                id: ASSET_LAYER_ID,
                type: "circle",
                source: ASSET_SOURCE_ID,
                paint:{
                    "circle-radius":6,
                    "circle-color": "#2563a6",
                    "circle-stroke-color": "#f3f6fa",
                    "circle-stroke-width": 1.5,
                }
            })
        }
        map.on("load",handleMapLoad)
        mapRef.current = map
        
        return ()=>{
            map.off("load",handleMapLoad)
            map.remove()
            mapRef.current = null
        }
    },[])

    useEffect(()=>{
        const map = mapRef.current
        if (!map){
            return
        }
        const source: maplibregl.GeoJSONSource = map.getSource(ASSET_SOURCE_ID)
        if(source){
            source.setData(assetCollection)
        }
    },[assetCollection])
    return (<div ref={container} className="asset-map"></div>)
}