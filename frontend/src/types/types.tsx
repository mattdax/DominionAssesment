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
    patrolPaths: PatrolPath[];
    activePatrolPathId: string | null;
}
