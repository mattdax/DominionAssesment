import type { Point, Feature } from 'geojson'
import type { AutonomousDrone, DroneMode } from '../types/types'

type DroneProperties = {
	assetId: string
	heading: number
	speed: number
	mode: DroneMode
	targetId: string | null
}

export function droneToGeo(drone: AutonomousDrone): Feature<Point, DroneProperties> {
	return {
		type: 'Feature',
		properties: {
			assetId: drone.assetId,
			heading: drone.heading,
			speed: drone.speed,
			mode: drone.mode,
			targetId: drone.targetId
		},
		geometry: {
			type: 'Point',
			coordinates: [drone.longitude, drone.latitude]
		}
	}
}
