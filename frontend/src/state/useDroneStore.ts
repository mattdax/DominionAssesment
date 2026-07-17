import type { AutonomousDrone } from "../types/types"
import { create } from "zustand"

type DroneActions ={
    setDrone: (drone: AutonomousDrone)=> void,
    clearDrone: () => void
}

function createInitialDroneState(){
    return {drone: null as AutonomousDrone | null}
}

type DroneState = ReturnType<typeof createInitialDroneState>

export type DroneStore = DroneState & DroneActions;

export const useDroneStore = create<DroneStore>()((set)=>({...createInitialDroneState(),
    setDrone: (drone) =>{
        set({drone})
    },
    clearDrone: () =>{
        set(createInitialDroneState())
    }
}))