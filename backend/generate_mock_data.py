import numpy as np
import rasterio
from rasterio.transform import from_origin
import os

# Ensure data directory exists
os.makedirs('../data', exist_ok=True)

# Parameters for mock hyperspectral cube
width, height = 256, 256
num_bands = 200 # Simulating hyperspectral depth

print(f"Generating mock {num_bands}-band hyperspectral image...")
# Generate random noise (simulating spectral reflectance)
# Shape is (Bands, Height, Width) for Rasterio standard
mock_data = np.random.rand(num_bands, height, width).astype('float32')

# Inject an artificial "disease anomaly" in the center of band 150
# We will train the model to find this specific pattern later!
mock_data[150, 100:150, 100:150] += 0.5 

# Define geospatial metadata (Dummy GPS coordinates)
transform = from_origin(-120.0, 35.0, 0.0001, 0.0001)

# Save as a multi-band GeoTIFF
filepath = '../data/mock_hyperspectral.tif'
with rasterio.open(
    filepath,
    'w',
    driver='GTiff',
    height=height,
    width=width,
    count=num_bands,
    dtype=mock_data.dtype,
    crs='+proj=latlong',
    transform=transform,
) as dst:
    dst.write(mock_data)

print(f"Success! Mock hyperspectral GeoTIFF saved to {filepath}.")