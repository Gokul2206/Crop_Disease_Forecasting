import React from 'react';
import DeckGL from '@deck.gl/react';
import { Map } from 'react-map-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

// 1. PASTE YOUR MAPBOX TOKEN HERE
// This authorizes your app to download satellite tiles
const MAPBOX_ACCESS_TOKEN = 'pk.YOUR_TOKEN_HERE';

// 2. SET THE CAMERA (INITIAL VIEW STATE)
// We are pointing the camera at a random agricultural area in California
const INITIAL_VIEW_STATE = {
  longitude: -120.0,  // X-coordinate
  latitude: 35.0,     // Y-coordinate
  zoom: 13,           // How close to the ground we are
  pitch: 45,          // Tilts the camera for a 3D perspective
  bearing: 0          // Rotation (0 is North-up)
};

export default function App() {
  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative' }}>
      
      {/* 
        3. THE DECK.GL CANVAS
        This acts as the transparent 3D layer. We enable the controller 
        so the user can click and drag to pan, and right-click to tilt/rotate.
      */}
      <DeckGL
        initialViewState={INITIAL_VIEW_STATE}
        controller={true}
      >
        {/* 
          4. THE BASE MAPBOX LAYER
          This renders the real-world satellite imagery underneath our Deck.gl glass.
        */}
      </DeckGL>

      {/* 5. BASIC UI OVERLAY */}
      <div style={uiStyle}>
        <h2 style={{ margin: '0 0 10px 0' }}>TerraSpectra GIS</h2>
        <p style={{ margin: 0, fontSize: '14px', color: '#ccc' }}>
          Base map loaded. Ready for ML heatmap ingestion.
        </p>
      </div>
    </div>
  );
}

// Simple styling for the UI box
const uiStyle = {
  position: 'absolute',
  top: 20,
  left: 20,
  zIndex: 1, // Ensures the UI sits above the map
  background: 'rgba(20, 20, 20, 0.85)',
  color: 'white',
  padding: '20px',
  borderRadius: '8px',
  fontFamily: 'system-ui, sans-serif',
  border: '1px solid #333'
};