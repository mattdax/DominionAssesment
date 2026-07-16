import { io } from "socket.io-client";
import type { Asset } from "../types/types";
import { useEffect } from "react";
import { SERVER_HOST, SERVER_PORT } from "../config/config";
import { useAssetStore } from "../state/useAssetStore";
type AssetsPayload = {
    assets: Asset[]
}

export function useAssetSocket(enabled=true){
    const setAssets = useAssetStore((state)=> state.setAssets)
    const applyUpdate = useAssetStore((state)=> state.applyUpdate)
    
    useEffect(()=>{
        if(!enabled){
            return
        }
        
        const socket = io("http://"+SERVER_HOST+":"+SERVER_PORT)
        
        const handleSnapshot = (payload: AssetsPayload) => {
            setAssets(payload.assets)
        }
        
        const handleUpdate = (payload: AssetsPayload)=>{
            applyUpdate(payload.assets)
        }
        socket.on("assets.snapshot",handleSnapshot)
        socket.on("assets.updated",handleUpdate)
        
        return ()=>{
            socket.off("assets.snapshot",handleSnapshot)
            socket.off("assets.updated",handleUpdate)
            socket.disconnect()
        }
    },[enabled,setAssets,applyUpdate])
}