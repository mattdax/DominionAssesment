import type { Feature, LineString,Polygon } from "geojson"


export type Asset ={
    assetId: string,
    assetType: string,
    longitude: number,
    latitude: number,
    sequence: number,
    heading: number,
    speed:number,
    timestamp: string
    analysis: AssetAnalysis
}

export type RestrictedZone = Feature<Polygon, {
    kind: "restricted-zone",
    name?: string
}> & {id: string}

export type PatrolPath = Feature<LineString, {
    kind: "patrol-path",
    name?: string
}> & {id: string}

export type AddedTool = {
    zones: RestrictedZone[],
    patrolPaths: PatrolPath[],
    activePatrolPathId: string | null
}

export type ThreatLevel = "normal" | "warning" | "critical"

export type AssetAnalysis= {
    assetId: string,
    isInsideZone: boolean,
    nearestZoneId: string | null,
    distanceToZone: number | null,
    entryZoneId: string | null,
    tte: number | null,
    threatLevel: ThreatLevel
}

export type DroneMode = "idle"| "patrol"|"intercept"|"shadow"

export type AutonomousDrone = {
    assetId: string,
    assetType: string,
    longitude: number,
    latitude: number,
    sequence: number,
    heading: number,
    speed: number,
    timestamp: string,
    mode: DroneMode,
    targetId: string | null
}