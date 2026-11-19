import React, { useEffect, useRef } from 'react';
import mapboxgl from 'mapbox-gl';
import { MapboxOverlay } from '@deck.gl/mapbox';
import { GridLayer } from '@deck.gl/aggregation-layers';
import 'mapbox-gl/dist/mapbox-gl.css';

import mockData from './mock_disease_data.json';

const FREE_SATELLITE_STYLE = {
  version: 8,
  sources: {
    'esri-satellite': {
      type: 'raster',
      tiles: [
        'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
      ],
      tileSize: 256,
      maxzoom: 15 // Prevents black squares by smoothly upscaling tiles when zoomed in
    }
  },
  layers: [
    {
      id: 'satellite-layer',
      type: 'raster',
      source: 'esri-satellite'
    }
  ]
};

export default function App() {
  const mapContainer = useRef(null);
  const mapRef = useRef(null);

  useEffect(() => {
    if (mapRef.current) return;

    const map = new mapboxgl.Map({
      container: mapContainer.current,
      style: FREE_SATELLITE_STYLE,
      // Satisfies the Mapbox engine's kill switch so it doesn't delete the ESRI map
      accessToken: import.meta.env.VITE_MAPBOX_TOKEN,
      center: [-120.0, 35.0],
      zoom: 14,
      pitch: 55,
      bearing: 15,
      antialias: true
    });

    const overlay = new MapboxOverlay({
      interleaved: false, // Prevents WebGL depth clashes that cause black tile patches
      layers: [
        new GridLayer({
          id: 'disease-heatmap',
          data: mockData,
          pickable: true,
          extruded: true,
          cellSize: 100,
          coverage: 0.85,
          elevationRange: [20, 180], // Caps max bar height to 180m (default is 1000m)
          elevationScale: 1,
          elevationAggregation: 'MEAN',
          colorAggregation: 'MEAN',
          getPosition: d => [d.lng, d.lat],
          getElevationWeight: d => d.stress_level,
          getColorWeight: d => d.stress_level,
          colorRange: [
            [0, 220, 100, 170],
            [255, 210, 0, 210],
            [255, 45, 45, 240]
          ]
        })
      ]
    });

    map.addControl(overlay);
    mapRef.current = map;

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative', overflow: 'hidden' }}>
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