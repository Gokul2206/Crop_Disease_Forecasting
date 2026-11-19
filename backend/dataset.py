import torch
from torch.utils.data import Dataset, DataLoader
import rasterio
import numpy as np

class HyperspectralDataset(Dataset):
    def __init__(self, tiff_filepath, label_filepath='../data/mock_labels.npy', transform=None):
        """
        Loads the PCA-reduced GeoTIFF and its matching ground-truth label map.
        """
        self.filepath = tiff_filepath
        self.transform = transform

        with rasterio.open(self.filepath) as src:
            self.image_data = src.read()  # Shape: (30, H, W)

        self.label_map = np.load(label_filepath)  # Shape: (H, W)
        self.patches, self.labels = self._extract_patches(self.image_data, self.label_map, patch_size=32)

    def _extract_patches(self, img_array, label_map, patch_size):
        """
        Slices the (30, H, W) map and (H, W) labels into aligned 32x32 patches.
        """
        _, h, w = img_array.shape
        patches = []
        patch_labels = []

        for i in range(0, h - patch_size + 1, patch_size):
            for j in range(0, w - patch_size + 1, patch_size):
                patch = img_array[:, i:i+patch_size, j:j+patch_size]
                lbl_patch = label_map[i:i+patch_size, j:j+patch_size]
                
                # Assign the dominant class label in this 32x32 patch
                dominant_label = np.bincount(lbl_patch.ravel()).argmax()
                patches.append(patch)
                patch_labels.append(dominant_label)

        return patches, torch.tensor(patch_labels, dtype=torch.long)

    def __len__(self):
        return len(self.patches)

    def __getitem__(self, idx):
        x = torch.tensor(self.patches[idx], dtype=torch.float32)
        y = self.labels[idx]

        if self.transform:
            x = self.transform(x)

        return x, y

if __name__ == "__main__":
    print("🚜 TerraSpectra: Testing Week 2 PyTorch DataLoader with Real Ground-Truth Labels...")

    dataset = HyperspectralDataset('../data/reduced_hyperspectral.tif')
    dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

    # Print real class distribution across the 64 farm patches
    counts = torch.bincount(dataset.labels, minlength=3)
    print(f"Total Patches: {len(dataset)} -> Healthy: {counts[0]}, Moderate Stress: {counts[1]}, Severe Blight: {counts[2]}")

    sample_batch, sample_labels = next(iter(dataloader))
    print(f"Batch Tensor Shape: {sample_batch.shape}")
    print(f"Sample Batch Labels: {sample_labels.tolist()}")