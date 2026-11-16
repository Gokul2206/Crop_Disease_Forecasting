import React from 'react';
import DeckGL from '@deck.gl/react';
import { Map } from 'react-map-gl/mapbox';
import { GridLayer } from '@deck.gl/aggregation-layers';
import 'mapbox-gl/dist/mapbox-gl.css';

// Import our mock ML data
import mockData from './mock_disease_data.json';

const MAPBOX_ACCESS_TOKEN = 'pk.YOUR_TOKEN_HERE'; 

const INITIAL_VIEW_STATE = {
  longitude: -120.0,
  latitude: 35.0,
  zoom: 14, // Zoomed in a bit closer to see the grid
  pitch: 60,
  bearing: 15
};

export default function App() {
  
  // Create the Deck.gl Heatmap Layer
  const layers = [
    new GridLayer({
      id: 'disease-heatmap',
      data: mockData,
      pickable: true,
      extruded: true, // This makes the grid cells 3D (pop out of the map)
      cellSize: 100, // Size of each grid block in meters
      elevationScale: 50, // How tall the 3D bars get
      getPosition: d => [d.lng, d.lat],
      getElevationWeight: d => d.stress_level,
      getColorWeight: d => d.stress_level,
      // Colors go from Green (healthy) to Red (high stress)
      colorRange: [
        [0, 255, 0, 150],     // Low stress
        [255, 255, 0, 200],   // Medium stress
        [255, 0, 0, 255]      // High stress (Fungal Blight!)
      ]
    })
  ];

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative' }}>
      <DeckGL
        initialViewState={INITIAL_VIEW_STATE}
        controller={true}
        layers={layers} // Inject our heatmap layer here!
        getTooltip={({object}) => object && `Stress Level: ${object.elevationValue}`}
      >
      </DeckGL>

      <div style={uiStyle}>
        <h2 style={{ margin: '0 0 10px 0', color: '#ff4d4d' }}>🚨 Anomaly Detected</h2>
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