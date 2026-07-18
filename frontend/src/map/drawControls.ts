import { MaplibreTerradrawControl } from '@watergis/maplibre-gl-terradraw'
import '@watergis/maplibre-gl-terradraw/dist/maplibre-gl-terradraw.css'

// Draw Controller
export function drawControls() {
	return new MaplibreTerradrawControl({
		modes: ['linestring', 'polygon', 'select', 'delete-selection', 'delete'],
		open: true
	})
}
