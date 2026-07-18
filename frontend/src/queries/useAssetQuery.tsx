import { useQuery } from "@tanstack/react-query"
import { fetchAssets } from "../api/fetchAssets"

export function useAssetQuery() {
	const query = useQuery({
		queryKey: ["assets"],
		queryFn: ({ signal }) => fetchAssets(signal),
		staleTime: 10_000
	})
	return query
}
