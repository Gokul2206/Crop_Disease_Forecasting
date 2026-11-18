import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

# Import the components you built today
from dataset import HyperspectralDataset
from model import Hyperspectral3DCNN

print("🚀 TerraSpectra: Initializing Week 2 Training Pipeline...")

# 1. Load the Data
dataset = HyperspectralDataset('../data/reduced_hyperspectral.tif')
dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

# 2. Initialize Model, Loss Function, and Optimizer
model = Hyperspectral3DCNN(num_classes=3)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 3. The Training Loop
epochs = 5
print(f"Beginning training for {epochs} epochs...\n")

for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    
    for batch_idx, (inputs, labels) in enumerate(dataloader):
        # Clear old gradients
        optimizer.zero_grad()
        
        # Forward Pass: Predict the health class
        outputs = model(inputs)
        
        # Compute the error (Loss)
        loss = criterion(outputs, labels)
        
        # Backward Pass: Calculate how to fix the error
        loss.backward()
        
        # Update Model Weights
        optimizer.step()
        
        running_loss += loss.item()
        
    # Calculate average loss for this epoch
    avg_loss = running_loss / len(dataloader)
    print(f"Epoch [{epoch+1}/{epochs}] - Loss: {avg_loss:.4f}")

print("\n✅ Training Complete! The 3D-CNN has learned the hyperspectral patterns.")

# Save the trained model weights so the React frontend can use them later
torch.save(model.state_dict(), 'terraspectra_weights.pth')
print("💾 Model saved to 'terraspectra_weights.pth'")