import type { LineLayerSpecification } from "maplibre-gl";

export const HISTORY_SOURCE_ID = "asset-history"
export const HISTORY_LAYER_ID = "asset-history-line"
export const PREDICTION_SOURCE_ID = "asset-prediction"
export const PREDICTION_LAYER_ID = "asset-prediction-line"

export function HistoryLayer(): LineLayerSpecification{
    return {
        id: HISTORY_LAYER_ID,
        type:"line",
        source:HISTORY_SOURCE_ID,

        layout:{
            "line-cap": "round",
            "line-join": "round"
        },
        paint:{
            "line-color": "#475569",
            "line-width": 3,
            "line-opacity": 0.35
        }
    }
}

export function PredictionLayer(): LineLayerSpecification{
    return {
        id: PREDICTION_LAYER_ID,
        type:"line",
        source:PREDICTION_SOURCE_ID,
        layout:{
            "line-cap": "round",
            "line-join": "round"
        },
        paint:{
            "line-color": "#0284c7",
            "line-width": 3,
            "line-opacity": 0.85,
            "line-dasharray": [2, 2]
        }
    }
}