import os
import json
import random
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from PIL import Image

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as T
import torchvision.models as models
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ---------- Paths ----------
DATA_DIR = Path("./data")
TRAIN_IMG_DIR = DATA_DIR / "train"
TEST_IMG_DIR = DATA_DIR / "test"
TRAIN_ANN_PATH = DATA_DIR / "iwildcam2020_train_annotations.json"
SUBMISSION_PATH = Path("./submission.csv")

# ---------- Load annotations ----------
with open(TRAIN_ANN_PATH, "r") as f:
    train_ann = json.load(f)

# Build image_id -> category_id mapping (first annotation per image)
img2cat_raw = {}
for ann in train_ann["annotations"]:
    img_id = ann["image_id"]
    if img_id not in img2cat_raw:
        img2cat_raw[img_id] = ann["category_id"]

# Create contiguous label space
unique_cats = sorted(set(img2cat_raw.values()))
cat2idx = {cat: i for i, cat in enumerate(unique_cats)}
idx2cat = {i: cat for cat, i in cat2idx.items()}
num_classes = len(unique_cats)

# Gather training files and label indices
train_files, train_labels = [], []
for fname in os.listdir(TRAIN_IMG_DIR):
    if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
        continue
    img_id = Path(fname).stem
    if img_id in img2cat_raw:
        train_files.append(TRAIN_IMG_DIR / fname)
        train_labels.append(cat2idx[img2cat_raw[img_id]])

print(f"Total labeled images found: {len(train_files)}  |  Classes: {num_classes}")

# Optional: limit number of samples for speed (keep stratification)
MAX_TRAIN_SAMPLES = 60000
if len(train_files) > MAX_TRAIN_SAMPLES:
    # stratified sampling
    indices = np.arange(len(train_files))
    train_idx, _ = train_test_split(
        indices,
        train_size=MAX_TRAIN_SAMPLES,
        stratify=train_labels,
        random_state=42,
    )
    train_files = [train_files[i] for i in train_idx]
    train_labels = [train_labels[i] for i in train_idx]
    print(f"Sampled down to {len(train_files)} images for faster training.")

# ---------- Train/validation split (stratified) ----------
train_idx, val_idx = train_test_split(
    np.arange(len(train_files)),
    test_size=0.2,
    random_state=42,
    stratify=train_labels,
)
train_files_split = [train_files[i] for i in train_idx]
train_labels_split = [train_labels[i] for i in train_idx]
val_files_split = [train_files[i] for i in val_idx]
val_labels_split = [train_labels[i] for i in val_idx]


# ---------- Dataset ----------
class ImgDataset(Dataset):
    def __init__(self, files, labels, transform=None):
        self.files = files
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        path = self.files[idx]
        img = Image.open(path).convert("RGB")
        if self.transform:
            img = self.transform(img)
        label = self.labels[idx]
        return img, label


transform = T.Compose(
    [
        T.Resize(256),
        T.CenterCrop(224),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

train_dataset = ImgDataset(train_files_split, train_labels_split, transform)
val_dataset = ImgDataset(val_files_split, val_labels_split, transform)

BATCH_SIZE = 32
NUM_WORKERS = 2

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=NUM_WORKERS,
    pin_memory=True,
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=NUM_WORKERS,
    pin_memory=True,
)

# ---------- Model ----------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.mobilenet_v2(pretrained=True)

# Freeze feature extractor
for param in model.features.parameters():
    param.requires_grad = False

# Replace classifier
in_features = model.classifier[1].in_features
model.classifier[1] = nn.Linear(in_features, num_classes)

model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()), lr=1e-3
)

# ---------- Training ----------
EPOCHS = 3
for epoch in range(1, EPOCHS + 1):
    model.train()
    running_loss = 0.0
    for imgs, labs in tqdm(train_loader, desc=f"Epoch {epoch}/{EPOCHS} [train]"):
        imgs = imgs.to(device, non_blocking=True)
        labs = labs.to(device, non_blocking=True)

        optimizer.zero_grad()
        outputs = model(imgs)
        loss = criterion(outputs, labs)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * imgs.size(0)

    epoch_loss = running_loss / len(train_dataset)

    # Validation
    model.eval()
    all_preds, all_true = [], []
    with torch.no_grad():
        for imgs, labs in tqdm(val_loader, desc=f"Epoch {epoch}/{EPOCHS} [val]"):
            imgs = imgs.to(device, non_blocking=True)
            labs = labs.to(device, non_blocking=True)
            outputs = model(imgs)
            preds = outputs.argmax(dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_true.extend(labs.cpu().numpy())
    val_acc = accuracy_score(all_true, all_preds)
    print(f"Epoch {epoch}: Train loss {epoch_loss:.4f} | Val Accuracy {val_acc:.4f}")

print(f"Final validation accuracy: {val_acc:.4f}")

# ---------- Predict on test set ----------
test_files = sorted(
    [p for p in TEST_IMG_DIR.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"}]
)
test_dataset = ImgDataset(test_files, [0] * len(test_files), transform)
test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=NUM_WORKERS,
    pin_memory=True,
)

model.eval()
test_preds_idx = []
with torch.no_grad():
    for imgs, _ in tqdm(test_loader, desc="Predict test"):
        imgs = imgs.to(device)
        outputs = model(imgs)
        preds = outputs.argmax(dim=1).cpu().numpy()
        test_preds_idx.extend(preds)

# Map back to original category IDs
test_preds = [idx2cat[idx] for idx in test_preds_idx]

# Build and save submission
submission = pd.DataFrame({"Id": [p.stem for p in test_files], "Predicted": test_preds})
submission.to_csv(SUBMISSION_PATH, index=False)
print(f"Submission saved to {SUBMISSION_PATH}")
