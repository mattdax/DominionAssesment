import { socket } from "./socket";
import type { Asset, PatrolPath, RestrictedZone } from "../types/types";
import { useEffect } from "react";
import { useAssetStore } from "../state/useAssetStore";
import { useAddedToolStore } from "../state/useAddedToolStore";
import { useDroneStore } from "../state/useDroneStore";
import type { AddedTool, AutonomousDrone } from "../types/types";

type AssetsPayload = {
    assets: Asset[]
}
type ZonePayload = {
    zone: RestrictedZone
}
type ZoneDeletedPayload = {
    zoneId: string
}
type PathPayload = {
    path: PatrolPath
}
type PathDeletedPayload = {
    pathId: string
}
type ActivePathPayload = {
    pathId: string | null
}
type DronePayload = {
    drone: AutonomousDrone
}

export function useSocket(enabled=true){
    const setAssets = useAssetStore((state)=> state.setAssets)
    const applyUpdate = useAssetStore((state)=> state.applyUpdate)
    const setToolSnapshot = useAddedToolStore((state)=>state.setSnapshot)
    const addZone = useAddedToolStore((state)=>state.addZone)
    const addPath = useAddedToolStore((state)=>state.addPath)
    const removeZone = useAddedToolStore((state)=>state.removeZone)
    const removePath = useAddedToolStore((state)=>state.removePath)
    const setActivePatrolPath = useAddedToolStore((state)=>state.setActivePatrolPath)
    const setDrone = useDroneStore((state)=>state.setDrone)


    useEffect(()=>{
        if(!enabled){
            return
        }
        
        const handleAssetSnapshot = (payload: AssetsPayload) => {
            setAssets(payload.assets)
        }
        
        const handleAssetUpdate = (payload: AssetsPayload)=>{
            applyUpdate(payload.assets)
        }
        const handleToolSnapshot = (payload: AddedTool)=>{
            setToolSnapshot(payload)
        }
        const handleAddZone = (payload: ZonePayload)=>{
            addZone(payload.zone)
        }
        const handleAddPath = (payload: PathPayload)=>{
            addPath(payload.path)
        }
        const handleRemoveZone = (payload: ZoneDeletedPayload)=>{
            removeZone(payload.zoneId)
        }
        const handleRemovePath = (payload: PathDeletedPayload)=>{
            removePath(payload.pathId)
        }
        const handleActivePath = (payload: ActivePathPayload)=>{
            setActivePatrolPath(payload.pathId)
        }
        const handleDroneState = (payload: DronePayload)=>{
            setDrone(payload.drone)
        }
        socket.on("assets.snapshot",handleAssetSnapshot)
        socket.on("assets.updated",handleAssetUpdate)
        
        socket.on("tools.snapshot",handleToolSnapshot)
        socket.on("zone.inserted",handleAddZone)
        socket.on("zone.deleted",handleRemoveZone)
        socket.on("path.inserted",handleAddPath)
        socket.on("path.deleted",handleRemovePath)
        socket.on("path.activated",handleActivePath)
        socket.on("autonomous-drone.snapshot",handleDroneState)
        socket.on("autonomous-drone.updated",handleDroneState)
        socket.connect();

        return ()=>{
            socket.off("assets.snapshot",handleAssetSnapshot)
            socket.off("assets.updated",handleAssetUpdate)

            socket.off("tools.snapshot",handleToolSnapshot)
            socket.off("zone.inserted",handleAddZone)
            socket.off("zone.deleted",handleRemoveZone)
            socket.off("path.inserted",handleAddPath)
            socket.off("path.deleted",handleRemovePath)
            socket.off("path.activated",handleActivePath)
            socket.off("autonomous-drone.snapshot",handleDroneState)
            socket.off("autonomous-drone.updated",handleDroneState)
            socket.disconnect()
        }
    },[enabled,setAssets,applyUpdate,addPath,addZone,removePath,removeZone,setActivePatrolPath,setToolSnapshot,setDrone])
}