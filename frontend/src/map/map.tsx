import { useEffect, useRef } from "react"
import maplibregl from "maplibre-gl"
import "maplibre-gl/dist/maplibre-gl.css"
import "./map.css"

export function AssetMap(){
    const container = useRef<HTMLDivElement | null>(null)
    const mapRef = useRef<maplibregl.Map | null> (null)
    
    useEffect(()=>{
        // if div container does not exist stop
        if(!container.current || mapRef.current){
            return
        }
        const map = new maplibregl.Map({container: container.current, 
                    style: "https://tiles.openfreemap.org/styles/liberty",
                    center: [-75.6972, 45.4215],
                    zoom: 9    
                })
        map.addControl(new maplibregl.NavigationControl(),"top-left")
        mapRef.current = map
        return ()=>{
            map.remove()
            mapRef.current = null
        }
    },[])
    return (<div ref={container} className="asset-map"></div>)
}