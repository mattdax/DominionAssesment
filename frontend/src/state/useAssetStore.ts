import { create } from 'zustand'
import { createInitialAssetState } from './useAssetStoreHelpers'
import type { Asset } from '../types/types'

// Store actions
type AssetActions = {
	setAssets: (assets: Asset[]) => void
	applyUpdate: (assets: Asset[]) => void
	clearAssets: () => void
	selectAsset: (assetId: string) => void
	clearSelectedAsset: () => void
}
// Create Store type
type AssetState = ReturnType<typeof createInitialAssetState>
export type AssetStore = AssetState & AssetActions

// Create Store
export const useAssetStore = create<AssetStore>()((set) => ({
	...createInitialAssetState(),
	setAssets: (assets) => {
		const mapped = assets.map((asset) => [asset.assetId, asset])
		set({ assetsById: Object.fromEntries(mapped) })
	},
	applyUpdate: (assets) => {
		set((state) => {
			const byIds = { ...state.assetsById }
			for (const asset of assets) {
				const currentAsset = byIds[asset.assetId]
				if (!currentAsset || asset.sequence > currentAsset.sequence) {
					byIds[asset.assetId] = asset
				}
			}
			return { assetsById: byIds }
		})
	},
	clearAssets: () => {
		set(createInitialAssetState())
	},
	selectAsset: (assetId) => set({ selectedAssetId: assetId }),

	clearSelectedAsset: () => set({ selectedAssetId: null })
}))
