import torch
from torch.utils.data import Dataset, DataLoader
import rasterio
import numpy as np

class HyperspectralDataset(Dataset):
    def __init__(self, tiff_filepath, transform=None):
        """
        Loads the PCA-reduced GeoTIFF generated in Week 1.
        """
        self.filepath = tiff_filepath
        self.transform = transform
        
        # Load the reduced 30-band image
        with rasterio.open(self.filepath) as src:
            # Shape: (Bands, Height, Width) -> (30, H, W)
            self.image_data = src.read()
            
        # We need to slice the large farm map into smaller ML training patches (e.g., 32x32 pixels)
        self.patches = self._extract_patches(self.image_data, patch_size=32)
        
        # Mock labels: 0 (Healthy), 1 (Moderate Stress), 2 (Severe Anomaly/Fungal Blight)
        self.labels = torch.randint(0, 3, (len(self.patches),))

    def _extract_patches(self, img_array, patch_size):
        """
        Slices the large (30, H, W) map into smaller (30, 32, 32) tensors for the CNN.
        """
        _, h, w = img_array.shape
        patches = []
        for i in range(0, h - patch_size + 1, patch_size):
            for j in range(0, w - patch_size + 1, patch_size):
                patch = img_array[:, i:i+patch_size, j:j+patch_size]
                patches.append(patch)
        return patches

    def __len__(self):
        return len(self.patches)

    def __getitem__(self, idx):
        # Convert the numpy patch to a PyTorch tensor (Float32 for ML training)
        x = torch.tensor(self.patches[idx], dtype=torch.float32)
        y = self.labels[idx]
        
        if self.transform:
            x = self.transform(x)
            
        return x, y

if __name__ == "__main__":
    print("🚜 TerraSpectra: Testing Week 2 PyTorch DataLoader...")
    
    # Load the compressed file you just generated
    dataset = HyperspectralDataset('../data/reduced_hyperspectral.tif')
    dataloader = DataLoader(dataset, batch_size=16, shuffle=True)
    
    # Verify the tensor shapes are ready for the Neural Network
    sample_batch, sample_labels = next(iter(dataloader))
    
    print(f"Batch Tensor Shape: {sample_batch.shape}") 
    print(f"Labels Shape: {sample_labels.shape}")