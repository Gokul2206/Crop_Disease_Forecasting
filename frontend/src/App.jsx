import React, { useEffect, useRef } from 'react';
// 1. We import the native Mapbox engine directly, bypassing the broken React wrapper entirely
import mapboxgl from 'mapbox-gl';
import { MapboxOverlay } from '@deck.gl/mapbox';
import { GridLayer } from '@deck.gl/aggregation-layers';
import 'mapbox-gl/dist/mapbox-gl.css';

import mockData from './mock_disease_data.json';

const MAPBOX_ACCESS_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN;

export default function App() {
  const mapContainer = useRef(null);
  
  useEffect(() => {
    // 2. Instantiate the native map. This guarantees the API requests will fire!
    const map = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/satellite-v9',
      accessToken: MAPBOX_ACCESS_TOKEN,
      center: [-120.0, 35.0],
      zoom: 14,
      pitch: 60,
      bearing: 15,
      antialias: true
    });

    // 3. Create the Deck.gl overlay with your 3D heatmap data
    const overlay = new MapboxOverlay({
      interleaved: true,
      layers: [
        new GridLayer({
          id: 'disease-heatmap',
          data: mockData,
          pickable: true,
          extruded: true, 
          cellSize: 100, 
          elevationScale: 50, 
          getPosition: d => [d.lng, d.lat],
          getElevationWeight: d => d.stress_level,
          getColorWeight: d => d.stress_level,
          colorRange: [
            [0, 255, 0, 150],     
            [255, 255, 0, 200],   
            [255, 0, 0, 255]      
          ]
        })
      ]
    });

    // 4. Inject the 3D bars natively into the Mapbox engine
    map.addControl(overlay);

    // Cleanup to prevent memory leaks during hot reloads
    return () => map.remove();
  }, []);

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative', overflow: 'hidden' }}>
      
      {/* The physical DOM container the map will attach to */}
      <div ref={mapContainer} style={{ width: '100%', height: '100%' }} />

      <div style={uiStyle}>
        <h2 style={{ margin: '0 0 10px 0', color: '#ff4d4d' }}>🚨 TerraSpectra Anomaly Detected</h2>
        <p style={{ margin: 0, fontSize: '14px', color: '#ccc' }}>
          Zone 4 shows severe chlorophyll degradation.<br/>
          <strong>Predicted: Fungal Blight (3 Weeks Out)</strong>
        </p>
      </div>
    </div>
  );
}

const uiStyle = {
  position: 'absolute',
  top: 20,
  left: 20,
  zIndex: 1,
  background: 'rgba(20, 20, 20, 0.9)',
  color: 'white',
  padding: '20px',
  borderRadius: '8px',
  fontFamily: 'system-ui, sans-serif',
  border: '1px solid #444',
  boxShadow: '0 4px 15px rgba(0,0,0,0.5)'
};