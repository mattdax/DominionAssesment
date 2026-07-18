import type { CircleLayerSpecification } from 'maplibre-gl'

export const DRONE_SOURCE_ID = 'autonomous-drone'
export const DRONE_LAYER_ID = 'autonomous-drone-circle'

export function DroneLayer(): CircleLayerSpecification {
	return {
		id: DRONE_LAYER_ID,
		type: 'circle',
		source: DRONE_SOURCE_ID,

		paint: {
			'circle-radius': [
				'match',
				['get', 'mode'],

				'idle',
				7,
				'intercept',
				11,
				'shadow',
				10,
				// Patrol radius
				9
			],

			'circle-color': [
				'match',
				['get', 'mode'],
				'idle',
				'#64748b',
				'intercept',
				'#9333ea',
				'shadow',
				'#6d28d9',

				// Patrol color
				'#7c3aed'
			],

			'circle-stroke-color': '#f8fafc',
			'circle-stroke-width': 2.5,
			'circle-opacity': 0.95,
			'circle-stroke-opacity': 1
		}
	}
}
