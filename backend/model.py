import torch
import torch.nn as nn
import torch.nn.functional as F

class Hyperspectral3DCNN(nn.Module):
    def __init__(self, num_classes=3):
        super(Hyperspectral3DCNN, self).__init__()
        
        # 1st 3D Convolutional Block
        # Expects input: (Batch, 1 Channel, 30 Bands, 32 Height, 32 Width)
        self.conv1 = nn.Conv3d(in_channels=1, out_channels=16, kernel_size=(3, 3, 3), padding=1)
        self.pool1 = nn.MaxPool3d(kernel_size=(2, 2, 2))
        
        # 2nd 3D Convolutional Block
        self.conv2 = nn.Conv3d(in_channels=16, out_channels=32, kernel_size=(3, 3, 3), padding=1)
        self.pool2 = nn.MaxPool3d(kernel_size=(2, 2, 2))
        
        # Fully Connected Layers for Classification
        # After two 2x2x2 pooling layers, the 30x32x32 patch shrinks to 7x8x8
        flattened_size = 32 * 7 * 8 * 8 
        self.fc1 = nn.Linear(flattened_size, 128)
        self.dropout = nn.Dropout(0.5) # Prevents overfitting on the mock data
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        # The DataLoader provides (Batch, Bands, H, W).
        # A 3D-CNN requires (Batch, Channels, Depth, H, W). 
        # We use unsqueeze(1) to add a single grayscale-style channel dimension.
        x = x.unsqueeze(1) 
        
        # Pass through spatial-spectral feature extractors
        x = self.pool1(F.relu(self.conv1(x)))
        x = self.pool2(F.relu(self.conv2(x)))
        
        # Flatten and classify
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        logits = self.fc2(x)
        
        return logits

if __name__ == "__main__":
    print("🧠 TerraSpectra: Compiling 3D-CNN Architecture...")
    
    # 1. Initialize the model
    model = Hyperspectral3DCNN(num_classes=3)
    print("Model initialized successfully.")
    
    # 2. Create a mock tensor matching your exact DataLoader output
    # (16 images, 30 spectral bands, 32x32 pixels)
    mock_batch = torch.randn(16, 30, 32, 32)
    print(f"Input Shape: {mock_batch.shape}")
    
    # 3. Perform a forward pass
    predictions = model(mock_batch)
    
    print(f"Output Shape: {predictions.shape}")
    print("✅ Forward pass successful! Architecture is stable.")