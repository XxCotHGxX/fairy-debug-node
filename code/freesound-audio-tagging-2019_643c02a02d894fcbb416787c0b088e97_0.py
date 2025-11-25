import os
import pandas as pd
import torch
import torchaudio
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import KFold
from sklearn.metrics import label_ranking_average_precision_score
import numpy as np
from timm.models import create_model
import torch.nn as nn


# Define the dataset class with Random Cropping
class AudioDataset(Dataset):
    def __init__(self, df, audio_dir, max_len=431):
        self.df = df
        self.audio_dir = audio_dir
        self.mel_spectrogram = torchaudio.transforms.MelSpectrogram(
            sample_rate=44100, n_fft=2048, hop_length=512, n_mels=128
        )
        self.max_len = max_len

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        fname = self.df.iloc[idx, 0]
        labels = self.df.iloc[idx, 1:]
        try:
            waveform, sample_rate = torchaudio.load(os.path.join(self.audio_dir, fname))
            if waveform.shape[0] > 1:
                waveform = waveform.mean(dim=0, keepdim=True)
            # Random Cropping
            if waveform.shape[1] > self.max_len * 512:
                start = np.random.randint(0, waveform.shape[1] - self.max_len * 512)
                waveform = waveform[:, start : start + self.max_len * 512]
            else:
                waveform = torch.nn.functional.pad(
                    waveform, (0, self.max_len * 512 - waveform.shape[1])
                )
            mel_spec = self.mel_spectrogram(waveform)
            mel_spec = mel_spec.squeeze(0)
        except Exception as e:
            print(f"Error loading {fname}: {e}")
            mel_spec = torch.zeros(128, self.max_len)
        labels = torch.tensor(labels.values.astype(np.float32))
        return mel_spec, labels


class MixupDataset(Dataset):
    def __init__(self, dataset, alpha=0.2):
        self.dataset = dataset
        self.alpha = alpha

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        mel_spec1, labels1 = self.dataset[idx]
        idx2 = np.random.randint(len(self.dataset))
        mel_spec2, labels2 = self.dataset[idx2]
        lam = np.random.beta(self.alpha, self.alpha)
        mixed_mel_spec = lam * mel_spec1 + (1 - lam) * mel_spec2
        mixed_labels = lam * labels1 + (1 - lam) * labels2
        return mixed_mel_spec, mixed_labels


# Define the training function
def train(model, device, loader, optimizer, criterion):
    model.train()
    total_loss = 0
    for batch in loader:
        inputs, labels = batch
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs.unsqueeze(1))
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(loader)


# Define the evaluation function
def evaluate(model, device, loader, criterion):
    model.eval()
    total_loss = 0
    predictions = []
    labels = []
    with torch.no_grad():
        for batch in loader:
            inputs, targets = batch
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs.unsqueeze(1))
            loss = criterion(outputs, targets)
            total_loss += loss.item()
            predictions.append(torch.sigmoid(outputs).cpu().numpy())
            labels.append(targets.cpu().numpy())
    predictions = np.concatenate(predictions)
    labels = np.concatenate(labels)
    score = label_ranking_average_precision_score(labels, predictions)
    return total_loss / len(loader), score


# Main function
def main():
    torch.manual_seed(42)
    np.random.seed(42)

    train_curated_df = pd.read_csv("./data/train_curated.csv")
    train_noisy_df = pd.read_csv("./data/train_noisy.csv")

    train_df = pd.concat([train_curated_df, train_noisy_df])

    labels = train_df["labels"].str.get_dummies(sep=",")
    train_df = pd.concat([train_df[["fname"]], labels], axis=1)

    model = create_model(
        "resnet50",
        pretrained=False,
        num_classes=80,
        in_chans=1,
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    criterion = torch.nn.BCEWithLogitsLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)

    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    scores = []

    for fold, (train_idx, val_idx) in enumerate(kf.split(train_df)):
        train_subset = train_df.iloc[train_idx]
        val_subset = train_df.iloc[val_idx]

        train_dataset = AudioDataset(train_subset, "./data/train_curated/")
        val_dataset = AudioDataset(val_subset, "./data/train_curated/")
        noisy_dataset = AudioDataset(train_subset, "./data/train_noisy/")
        train_dataset.df = pd.concat([train_dataset.df, noisy_dataset.df])
        train_dataset = MixupDataset(train_dataset)
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

        for epoch in range(10):
            train_loss = train(model, device, train_loader, optimizer, criterion)
            val_loss, score = evaluate(model, device, val_loader, criterion)
            print(
                f"Fold {fold+1}, Epoch {epoch+1}, Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}, Val Score: {score:.4f}"
            )

        scores.append(score)

    print(f"Average Score: {np.mean(scores):.4f}")

    test_dir = "./data/test/"
    test_fnames = os.listdir(test_dir)
    test_df = pd.DataFrame({"fname": test_fnames})
    test_labels = pd.DataFrame(np.zeros((len(test_fnames), 80)))
    test_df = pd.concat([test_df, test_labels], axis=1)
    test_dataset = AudioDataset(test_df, test_dir)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    predictions = []
    with torch.no_grad():
        for batch in test_loader:
            inputs, _ = batch
            inputs = inputs.to(device)
            outputs = model(inputs.unsqueeze(1))
            predictions.append(torch.sigmoid(outputs).cpu().numpy())

    predictions = np.concatenate(predictions)
    submission_df = pd.DataFrame(predictions, columns=[f"label_{i}" for i in range(80)])
    submission_df["fname"] = test_fnames
    submission_df = submission_df[["fname"] + [f"label_{i}" for i in range(80)]]
    submission_df.columns = ["fname"] + list(
        pd.read_csv("./data/sample_submission.csv").columns[1:]
    )
    submission_df.to_csv("./submission.csv", index=False)


if __name__ == "__main__":
    main()
