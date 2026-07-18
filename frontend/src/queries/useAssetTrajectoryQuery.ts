import { useQuery } from "@tanstack/react-query";
import { fetchAssetTrajectory } from "../api/fetchAssetTrajectory";

export function useAssetTrajectoryQuery(assetId: string | null){
    const query = useQuery({
        queryKey: ["asset-trajectory", assetId],   
        queryFn: ({signal}) => fetchAssetTrajectory(assetId!, signal),
        enabled: assetId !== null,
        refetchInterval: 5000})
    return query
}
