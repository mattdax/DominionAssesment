import { describe, expect, test } from 'vitest'

import type { AssetPrediction, AssetTrajectory } from '../types/types'
import { isAssetPrediction, isAssetTrajectory } from './assetTrajectoryValidator'

const validPrediction: AssetPrediction = {
	assetId: 'drone:1',
	averageHeading: 90,
	averageSpeed: 20,
	predictionSeconds: 300,
	coordinates: [
		[-75.6972, 45.4215],
		[-75.62, 45.4215]
	]
}

const validTrajectory: AssetTrajectory = {
	assetId: 'drone:1',
	history: [
		{
			longitude: -75.6972,
			latitude: 45.4215,
			heading: 90,
			speed: 20,
			sequence: 1,
			timestamp: '2026-07-17T12:00:00.000+00:00'
		}
	],
	prediction: validPrediction
}

describe('asset trajectory validator', () => {
	test('valid prediction and invalid coordinates', () => {
		const malformedPrediction = {
			...validPrediction,
			coordinates: [[-75.6972]]
		}
		expect(isAssetPrediction(validPrediction)).toBe(true)
		expect(isAssetPrediction(malformedPrediction)).toBe(false)
	})

	test('valid trajectory and invalid prediction', () => {
		const malformedTrajectory = {
			...validTrajectory,
			prediction: {
				...validPrediction,
				averageSpeed: 'fast'
			}
		}
		expect(isAssetTrajectory(validTrajectory)).toBe(true)
		expect(isAssetTrajectory(malformedTrajectory)).toBe(false)
	})
})
