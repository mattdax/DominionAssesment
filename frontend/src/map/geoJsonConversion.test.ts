import { describe, expect, test } from 'vitest'

import type { Asset, AssetTrajectory, AutonomousDrone } from '../types/types'
import { assetToGeo } from './assetToGeo'
import { droneToGeo } from './droneToGeo'
import { historyToGeo, predictionToGeo } from './trajectoryToGeo'

const asset: Asset = {
	assetId: 'drone:1',
	assetType: 'public',
	longitude: -75.6972,
	latitude: 45.4215,
	sequence: 1,
	heading: 90,
	speed: 20,
	timestamp: '2026-07-17T12:00:00.000+00:00',
	analysis: {
		assetId: 'drone:1',
		isInsideZone: false,
		nearestZoneId: 'zone-1',
		distanceToZone: 100,
		entryZoneId: 'zone-1',
		tte: 10,
		threatLevel: 'warning'
	}
}

const drone: AutonomousDrone = {
	assetId: 'auto:1',
	assetType: 'autonomous',
	longitude: -75.6972,
	latitude: 45.4215,
	sequence: 1,
	heading: 90,
	speed: 100,
	timestamp: '2026-07-17T12:00:00.000+00:00',
	mode: 'intercept',
	targetId: 'drone:1'
}

const trajectory: AssetTrajectory = {
	assetId: 'drone:1',
	history: [
		{
			longitude: -75.6972,
			latitude: 45.4215,
			heading: 90,
			speed: 20,
			sequence: 1,
			timestamp: '2026-07-17T12:00:00.000+00:00'
		},
		{
			longitude: -75.6872,
			latitude: 45.4216,
			heading: 90,
			speed: 20,
			sequence: 2,
			timestamp: '2026-07-17T12:00:01.000+00:00'
		}
	],
	prediction: null
}

describe('GeoJSON conversion', () => {
	test('Valid assetToGeo', () => {
		const feature = assetToGeo(asset)

		expect(feature.geometry.coordinates).toEqual([asset.longitude, asset.latitude])
		expect(feature.properties.threatLevel).toBe('warning')
	})

	test('Valid droneToGeo', () => {
		const feature = droneToGeo(drone)

		expect(feature.properties.mode).toBe('intercept')
		expect(feature.properties.targetId).toBe('drone:1')
	})

	test('Valid historyToGeo', () => {
		const collection = historyToGeo(trajectory)

		expect(collection.features[0]?.geometry.coordinates).toEqual([
			[-75.6972, 45.4215],
			[-75.6872, 45.4216]
		])
		expect(historyToGeo(undefined).features).toEqual([])
	})

	test('empty prediction collection', () => {
		expect(predictionToGeo(trajectory).features).toEqual([])
		expect(predictionToGeo(undefined).features).toEqual([])
	})
})
