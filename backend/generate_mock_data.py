import numpy as np
import rasterio
from rasterio.transform import from_origin
import os

os.makedirs('../data', exist_ok=True)

width, height = 256, 256
num_bands = 200

print(f"Generating realistic {num_bands}-band hyperspectral farm cube...")

# 1. Create a realistic vegetation spectral curve ("Red-Edge" reflectance jump)
bands = np.linspace(0, 1, num_bands).astype('float32')
healthy_curve = (0.2 + 0.6 / (1.0 + np.exp(-15.0 * (bands - 0.5)))).astype('float32')

# Add slight natural soil/canopy variation across pixels + small sensor noise
np.random.seed(42)
spatial_variation = np.random.uniform(0.92, 1.08, size=(1, height, width)).astype('float32')
sensor_noise = np.random.normal(0, 0.02, size=(num_bands, height, width)).astype('float32')

mock_data = healthy_curve[:, None, None] * spatial_variation + sensor_noise

# 2. Build a matching ground-truth label map (aligned to 32x32 patches)
# 0 = Healthy (outer border), 1 = Moderate Stress (halo), 2 = Severe Fungal Blight (center)
labels = np.zeros((height, width), dtype=np.int64)
labels[32:224, 32:224] = 1  # Moderate Stress zone
labels[64:192, 64:192] = 2  # Severe Anomaly hotspot (Zone 4)

# 3. Inject realistic biological disease signatures into the spectral bands
# Moderate Stress: Near-Infrared (NIR) bands 120-180 drop
mock_data[120:180, labels == 1] -= 0.25

# Severe Fungal Blight: Sharp NIR drop + chlorophyll degradation spike in Red bands 60-90
mock_data[120:180, labels == 2] -= 0.55
mock_data[60:90, labels == 2] += 0.25

mock_data = np.clip(mock_data, 0.0, 1.0).astype('float32')

# 4. Save GeoTIFF (Coordinates shifted to California Central Valley farmland)
transform = from_origin(-120.45, 36.75, 0.0001, 0.0001)
tif_path = '../data/mock_hyperspectral.tif'

with rasterio.open(
    tif_path,
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

# 5. Save ground-truth label mask so PyTorch trains on real targets, not random noise
label_path = '../data/mock_labels.npy'
np.save(label_path, labels)

print(f"✅ Saved GeoTIFF to {tif_path}")
print(f"✅ Saved ground-truth label mask to {label_path}")