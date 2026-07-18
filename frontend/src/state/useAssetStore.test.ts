import { beforeEach, describe, expect, test } from 'vitest'

import type { Asset } from '../types/types'
import { useAssetStore } from './useAssetStore'

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
		nearestZoneId: null,
		distanceToZone: null,
		entryZoneId: null,
		tte: null,
		threatLevel: 'normal'
	}
}

describe('useAssetStore', () => {
	beforeEach(() => {
		useAssetStore.getState().clearAssets()
	})

	test('stores an asset snapshot by asset ID', () => {
		useAssetStore.getState().setAssets([asset])

		expect(useAssetStore.getState().assetsById[asset.assetId]).toEqual(asset)
	})

	test('replaces an asset with a higher sequence update', () => {
		useAssetStore.getState().setAssets([asset])
		const updatedAsset = {
			...asset,
			longitude: -75.6872,
			sequence: asset.sequence + 1
		}

		useAssetStore.getState().applyUpdate([updatedAsset])

		expect(useAssetStore.getState().assetsById[asset.assetId]).toEqual(updatedAsset)
	})

	test('ignores asset updates with an equal or lower sequence', () => {
		useAssetStore.getState().setAssets([asset])
		const equalSequence = {
			...asset,
			longitude: -75.6872
		}
		const lowerSequence = {
			...asset,
			longitude: -75.6772,
			sequence: asset.sequence - 1
		}

		useAssetStore.getState().applyUpdate([equalSequence, lowerSequence])

		expect(useAssetStore.getState().assetsById[asset.assetId]).toEqual(asset)
	})
})
