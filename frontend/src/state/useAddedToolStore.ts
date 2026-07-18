import { create } from 'zustand'
import type { AddedTool, PatrolPath, RestrictedZone } from '../types/types'

function createInitialAddedTool(): AddedTool {
	return {
		zones: [],
		patrolPaths: [],
		activePatrolPathId: null
	}
}

// AddedToolStore actions
type AddedToolActions = {
	setSnapshot: (snapshot: AddedTool) => void

	addPath: (path: PatrolPath) => void
	addZone: (zone: RestrictedZone) => void

	removePath: (pathId: string) => void
	removeZone: (zoneId: string) => void

	setActivePatrolPath: (pathId: string | null) => void
	clearTools: () => void
}

// Create Store type
type AddedToolState = ReturnType<typeof createInitialAddedTool>
export type AddedToolStore = AddedToolState & AddedToolActions

export const useAddedToolStore = create<AddedToolStore>()((set) => ({
	...createInitialAddedTool(),
	setSnapshot: (snapshot) => {
		set(snapshot)
	},
	addPath: (path) => {
		set((state) => ({
			patrolPaths: [...state.patrolPaths.filter((exists) => exists.id !== path.id), path]
		}))
	},
	addZone: (zone) => {
		set((state) => ({
			zones: [...state.zones.filter((exists) => exists.id !== zone.id), zone]
		}))
	},
	removePath: (pathId) => {
		set((state) => ({
			patrolPaths: [...state.patrolPaths.filter((exists) => exists.id !== pathId)],

			// If deleted path is active patrol path, stop the patrol
			activePatrolPathId: state.activePatrolPathId === pathId ? null : state.activePatrolPathId
		}))
	},
	removeZone: (zoneId) => {
		set((state) => ({
			zones: [...state.zones.filter((exists) => exists.id !== zoneId)]
		}))
	},
	setActivePatrolPath: (pathId) => {
		set({ activePatrolPathId: pathId })
	},
	clearTools: () => {
		set(createInitialAddedTool())
	}
}))
