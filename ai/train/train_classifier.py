import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import numpy as np
from tqdm import tqdm

MODULATIONS = ["AM", "FM", "BPSK", "QPSK", "16QAM", "64QAM", "WBFM", "AM-SSB", "AM-DSB"]


class SignalClassifier(nn.Module):
    def __init__(self, num_classes: int = len(MODULATIONS)):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((4, 4)),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)


class SpectrogramDataset(Dataset):
    def __init__(self, data_path: str):
        self.data = np.load(data_path, allow_pickle=True)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        spectrogram = item["spectrogram"]
        label = item["label"]
        return torch.tensor(spectrogram, dtype=torch.float32).unsqueeze(0), torch.tensor(label, dtype=torch.long)


def train(data_path: str, epochs: int = 50, lr: float = 1e-3, batch_size: int = 64):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dataset = SpectrogramDataset(data_path)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=4)

    model = SignalClassifier().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.5)

    for epoch in range(epochs):
        model.train()
        total_loss, correct, total = 0, 0, 0
        for spectrograms, labels in tqdm(loader, desc=f"Epoch {epoch+1}/{epochs}"):
            spectrograms, labels = spectrograms.to(device), labels.to(device)
            outputs = model(spectrograms)
            loss = criterion(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            correct += (outputs.argmax(1) == labels).sum().item()
            total += labels.size(0)
        scheduler.step()
        acc = correct / total * 100
        print(f"Epoch {epoch+1}: Loss={total_loss/len(loader):.4f}, Acc={acc:.2f}%")

    torch.save(model.state_dict(), "models/classifier.pth")
    print("Model saved to models/classifier.pth")


if __name__ == "__main__":
    import os
    os.makedirs("models", exist_ok=True)
    train("data/processed/train_spectrograms.npy")
