import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import numpy as np
from tqdm import tqdm


class SNRRegressor(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((4, 4)),
        )
        self.regressor = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 4 * 4, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 1),
        )

    def forward(self, x):
        x = self.features(x)
        return self.regressor(x)


class SNRDataset(Dataset):
    def __init__(self, data_path: str):
        self.data = np.load(data_path, allow_pickle=True)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        return (
            torch.tensor(item["spectrogram"], dtype=torch.float32).unsqueeze(0),
            torch.tensor(item["snr"], dtype=torch.float32),
        )


def train(data_path: str, epochs: int = 50, lr: float = 1e-3, batch_size: int = 64):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dataset = SNRDataset(data_path)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=4)

    model = SNRRegressor().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for spectrograms, snr_values in tqdm(loader, desc=f"Epoch {epoch+1}/{epochs}"):
            spectrograms, snr_values = spectrograms.to(device), snr_values.to(device)
            outputs = model(spectrograms).squeeze()
            loss = criterion(outputs, snr_values)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}: MSE Loss={total_loss/len(loader):.4f}")

    torch.save(model.state_dict(), "models/regressor.pth")
    print("Model saved to models/regressor.pth")


if __name__ == "__main__":
    import os
    os.makedirs("models", exist_ok=True)
    train("data/processed/train_snr.npy")
