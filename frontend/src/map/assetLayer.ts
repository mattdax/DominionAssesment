import type { CircleLayerSpecification } from "maplibre-gl";

export const ASSET_SOURCE_ID = "public-assets"
export const ASSET_LAYER_ID = "public-assets-circles"

export function AssetLayer(): CircleLayerSpecification {
    return {
        id: ASSET_LAYER_ID,
        type:"circle",
        source: ASSET_SOURCE_ID,

        paint:{
            "circle-radius": ["case",["boolean",["feature-state", "selected"],false],
            9,6],
            "circle-color": ["case", ["boolean",["feature-state","selected"], false],
            "#d97706",
            "#2563a6"
            ],
            "circle-stroke-color": "#f3f6fa",
            "circle-stroke-width": 1.5,
        }

    }
}