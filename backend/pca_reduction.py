import rasterio
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os

def load_and_reshape_geotiff(filepath):
    """Reads a multi-band GeoTIFF and reshapes it for PCA."""
    print(f"Loading data from {filepath}...")
    with rasterio.open(filepath) as src:
        img_data = src.read()  # Shape: (Bands, Height, Width)
        metadata = src.meta
        
    bands, height, width = img_data.shape
    print(f"Original shape: {img_data.shape} (Bands, Height, Width)")
    
    # PCA requires 2D input: (Samples/Pixels, Features/Bands)
    # We flatten the spatial dimensions
    reshaped_data = img_data.transpose(1, 2, 0).reshape(-1, bands)
    print(f"Reshaped for PCA: {reshaped_data.shape} (Pixels, Bands)")
    
    return reshaped_data, img_data.shape, metadata

def apply_pca(data, original_shape, n_components=30):
    """Applies PCA to reduce spectral bands and keep the most variance."""
    print(f"Applying PCA to reduce from {original_shape[0]} to {n_components} components...")
    
    pca = PCA(n_components=n_components)
    reduced_data = pca.fit_transform(data)
    
    # Calculate how much information (variance) is retained
    variance_retained = np.sum(pca.explained_variance_ratio_) * 100
    print(f"Variance retained: {variance_retained:.2f}%")
    
    # Reshape back to image format: (Height, Width, New_Bands)
    _, height, width = original_shape
    reduced_img = reduced_data.reshape(height, width, n_components)
    
    # Transpose back to Rasterio format: (New_Bands, Height, Width)
    reduced_img = reduced_img.transpose(2, 0, 1)
    print(f"Final reduced image shape: {reduced_img.shape}")
    
    return reduced_img, pca.explained_variance_ratio_, pca

def save_reduced_geotiff(output_path, reduced_img, metadata):
    """Saves the PCA-reduced data as a new GeoTIFF."""
    # Update metadata to reflect the new number of bands
    metadata.update(count=reduced_img.shape[0], dtype=reduced_img.dtype)
    
    with rasterio.open(output_path, 'w', **metadata) as dst:
        dst.write(reduced_img)
    print(f"Saved reduced GeoTIFF to {output_path}")

if __name__ == "__main__":
    input_filepath = '../data/mock_hyperspectral.tif'
    output_filepath = '../data/reduced_hyperspectral.tif'
    
    # 1. Process the data
    flat_data, orig_shape, meta = load_and_reshape_geotiff(input_filepath)
    reduced_img, variance, pca_model = apply_pca(flat_data, orig_shape, n_components=30)
    
    # 2. Save the compressed data for Week 2 ML training
    save_reduced_geotiff(output_filepath, reduced_img, meta)
    
    # 3. Exploratory Data Analysis (EDA): Plot the cumulative explained variance
    os.makedirs('../docs', exist_ok=True)
    plt.figure(figsize=(8, 5))
    plt.plot(np.cumsum(variance) * 100, marker='o', linestyle='--')
    plt.xlabel('Number of Principal Components')
    plt.ylabel('Cumulative Explained Variance (%)')
    plt.title('PCA Analysis: Hyperspectral Band Reduction')
    plt.grid(True)
    
    plot_path = '../docs/pca_variance_plot.png'
    plt.savefig(plot_path)
    print(f"EDA Variance plot saved to {plot_path}")