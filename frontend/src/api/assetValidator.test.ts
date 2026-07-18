import { describe, expect, test } from 'vitest'

import type { Asset } from '../types/types'
import { isAsset } from './assetValidator'

const validAsset: Asset = {
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
		nearestZoneId: null,
		distanceToZone: null,
		entryZoneId: null,
		tte: null,
		threatLevel: 'normal'
	}
}

describe('isAsset', () => {
	test('accepts a complete valid asset', () => {
		expect(isAsset(validAsset)).toBe(true)
	})

	test('rejects an asset that is missing or improperly structure', () => {
		const missingAnalysis: Record<string, unknown> = { ...validAsset }
		delete missingAnalysis.analysis

		const malformedAnalysis = {
			...validAsset,
			analysis: {
				...validAsset.analysis,
				threatLevel: 'unknown'
			}
		}

		expect(isAsset(missingAnalysis)).toBe(false)
		expect(isAsset(malformedAnalysis)).toBe(false)
	})
})
