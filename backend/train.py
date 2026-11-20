import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
import matplotlib.pyplot as plt

from dataset import HyperspectralDataset
from model import Hyperspectral3DCNN

print("🚀 TerraSpectra: Initializing Week 2 Train/Validation Pipeline...")

# 1. Load dataset and create a reproducible 80/20 Train/Validation split
dataset = HyperspectralDataset('../data/reduced_hyperspectral.tif')
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size

generator = torch.Generator().manual_seed(42)
train_dataset, val_dataset = random_split(dataset, [train_size, val_size], generator=generator)

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False)

print(f"Dataset Split -> Train: {train_size} patches | Validation: {val_size} patches")

# 2. Initialize Model, Loss Function, and Optimizer
model = Hyperspectral3DCNN(num_classes=3)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 3. Training & Validation Loop
epochs = 8
train_losses, val_losses, val_accuracies = [], [], []

print(f"Beginning training for {epochs} epochs...\n")

for epoch in range(epochs):
    # --- Training Phase ---
    model.train()
    running_train_loss = 0.0

    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_train_loss += loss.item()

    avg_train_loss = running_train_loss / len(train_loader)
    train_losses.append(avg_train_loss)

    # --- Validation Phase ---
    model.eval()
    running_val_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in val_loader:
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            running_val_loss += loss.item()

            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

    avg_val_loss = running_val_loss / len(val_loader)
    val_acc = (correct / total) * 100.0
    val_losses.append(avg_val_loss)
    val_accuracies.append(val_acc)

    print(
        f"Epoch [{epoch+1}/{epochs}] - "
        f"Train Loss: {avg_train_loss:.4f} | "
        f"Val Loss: {avg_val_loss:.4f} | "
        f"Val Acc: {val_acc:.2f}%"
    )

# 4. Save Training Metrics Plot for Mid-Review Documentation
os.makedirs('../docs', exist_ok=True)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

ax1.plot(range(1, epochs + 1), train_losses, marker='o', label='Train Loss')
ax1.plot(range(1, epochs + 1), val_losses, marker='s', label='Val Loss')
ax1.set_title('3D-CNN Loss Curve')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Cross-Entropy Loss')
ax1.legend()
ax1.grid(True)

ax2.plot(range(1, epochs + 1), val_accuracies, marker='o', color='green', label='Val Accuracy')
ax2.set_title('Validation Accuracy (%)')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Accuracy (%)')
ax2.set_ylim(0, 105)
ax2.legend()
ax2.grid(True)

plot_path = '../docs/training_metrics.png'
plt.tight_layout()
plt.savefig(plot_path)
print(f"\n📊 Saved training metrics plot to {plot_path}")

# 5. Save Model Weights
torch.save(model.state_dict(), 'terraspectra_weights.pth')
print("💾 Model saved to 'terraspectra_weights.pth'")