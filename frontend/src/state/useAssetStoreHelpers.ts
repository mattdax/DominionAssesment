import type { Asset } from '../types/types'
export function createInitialAssetState() {
	return {
		assetsById: {} as Record<string, Asset>,
		connectionStatus: 'not connected' as const,
		selectedAssetId: null as string | null
	}
}
