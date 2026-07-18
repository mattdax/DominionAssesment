import { beforeEach, describe, expect, test } from 'vitest'

import type { PatrolPath, RestrictedZone } from '../types/types'
import { useAddedToolStore } from './useAddedToolStore'

const zone: RestrictedZone = {
	type: 'Feature',
	id: 'zone-1',
	geometry: {
		type: 'Polygon',
		coordinates: [
			[
				[-75.7, 45.4],
				[-75.6, 45.4],
				[-75.6, 45.5],
				[-75.7, 45.5],
				[-75.7, 45.4]
			]
		]
	},
	properties: {
		kind: 'restricted-zone'
	}
}

const path: PatrolPath = {
	type: 'Feature',
	id: 'path-1',
	geometry: {
		type: 'LineString',
		coordinates: [
			[-75.6972, 45.4215],
			[-75.6872, 45.4215]
		]
	},
	properties: {
		kind: 'patrol-path'
	}
}

describe('useAddedToolStore', () => {
	beforeEach(() => {
		useAddedToolStore.getState().clearTools()
	})

	test('stores an added restricted zone', () => {
		useAddedToolStore.getState().addZone(zone)
		expect(useAddedToolStore.getState().zones).toEqual([zone])
	})

	test('replaces a zone received with the same ID', () => {
		const updatedZone: RestrictedZone = {
			...zone,
			properties: {
				...zone.properties,
				name: 'Updated zone'
			}
		}
		useAddedToolStore.getState().addZone(zone)
		useAddedToolStore.getState().addZone(updatedZone)
		expect(useAddedToolStore.getState().zones).toEqual([updatedZone])
	})

	test('replaces a patrol path received with the same ID', () => {
		const updatedPath: PatrolPath = {
			...path,
			properties: {
				...path.properties,
				name: 'Updated path'
			}
		}
		useAddedToolStore.getState().addPath(path)
		useAddedToolStore.getState().addPath(updatedPath)
		expect(useAddedToolStore.getState().patrolPaths).toEqual([updatedPath])
	})

	test('clears the active patrol path ID when that path is removed', () => {
		useAddedToolStore.getState().addPath(path)
		useAddedToolStore.getState().setActivePatrolPath(path.id)

		useAddedToolStore.getState().removePath(path.id)

		expect(useAddedToolStore.getState().patrolPaths).toEqual([])
		expect(useAddedToolStore.getState().activePatrolPathId).toBeNull()
	})
})
