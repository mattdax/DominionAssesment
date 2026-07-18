import type { CircleLayerSpecification } from 'maplibre-gl'

export const ASSET_SOURCE_ID = 'public-assets'
export const ASSET_LAYER_ID = 'public-assets-circles'

export function AssetLayer(): CircleLayerSpecification {
	return {
		id: ASSET_LAYER_ID,
		type: 'circle',
		source: ASSET_SOURCE_ID,

		paint: {
			'circle-radius': ['case', ['boolean', ['feature-state', 'selected'], false], 9, 6],
			'circle-color': [
				'match',
				['get', 'threatLevel'],

				'warning',
				'#d97706',

				'critical',
				'#dc2626',

				'#2563a6'
			],
			'circle-stroke-color': [
				'case',
				['boolean', ['feature-state', 'selected'], false],
				'#172033',
				'#f3f6fa'
			],

			'circle-stroke-width': ['case', ['boolean', ['feature-state', 'selected'], false], 3, 1.5]
		}
	}
}
