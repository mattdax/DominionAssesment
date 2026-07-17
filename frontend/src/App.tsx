
import { useEffect } from 'react'
import './App.css'
import { useAssetQuery } from './queries/useAssetQuery'
import { useAssetStore } from './state/useAssetStore'
import { useSocket } from './realtime/useSocket'
import { AssetMap } from './map/map'
function App() {
  
  const {data: assets, isPending, isError, error} = useAssetQuery()
  const setAssets = useAssetStore((state)=>state.setAssets)
  // for testing
  const storedAssetCount = useAssetStore((state)=>Object.keys(state.assetsById).length)
  const storedAssets = useAssetStore((state)=>state.assetsById)
  const firstAsset = Object.values(storedAssets)[0];
  //const currentSequence = useAssetStore((state)=>state.assetsById["drone:0"].sequence)
  useEffect(()=>{
    if(assets){
      setAssets(assets)
    }
  },[assets,setAssets])

  useSocket(true);

  if (isError) return <p>{error.message}</p>
  if (isPending) return <p>Loading Assets...</p>
  return (
   
    <div>
      <AssetMap/>
    <p>Received: {assets.length} assets</p>
    <p> Assets in Zustand: {storedAssetCount} </p>
    <p>Current Sequence: {firstAsset?.sequence}</p>
    </div>
  )
}

export default App
