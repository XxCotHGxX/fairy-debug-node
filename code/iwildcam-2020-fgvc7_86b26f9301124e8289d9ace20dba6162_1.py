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
    if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue
    img_id = Path(fname).stem
    if img_id in img2cat_raw:
        #***BUG FIX*** - Validate image before adding to dataset (try both verify and convert)
        img_path = TRAIN_IMG_DIR / fname
        try:
            with Image.open(img_path) as img:
                img.verify()  # First verify basic integrity
                img.convert("RGB")  # Then try converting to catch convert-time failures
            train_files.append(img_path)
            train_labels.append(cat2idx[img2cat_raw[img_id]])
        except Exception as e:
            print(f"Skipping corrupted image: {img_path} - {e}")

print(f"Total labeled images found: {len(train_files)}  |  Classes: {num_classes}")

# Optional: limit number of samples for speed (keep stratification)
MAX_TRAIN_SAMPLES = 60000
if len(train_files) > MAX_TRAIN_SAMPLES:
    # Check if we can do stratified sampling
    from collections import Counter
    label_counts = Counter(train_labels)
    min_count = min(label_counts.values())
    
    # If any class has less than 2 samples, fall back to random sampling
    if min_count < 2:
        print(f"Warning: Minimum class count is {min_count}, falling back to random sampling")
        indices = np.arange(len(train_files))
        np.random.shuffle(indices)
        train_idx = indices[:MAX_TRAIN_SAMPLES]
    else:
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
# Check if we can do stratified sampling on training data
from collections import Counter
label_counts = Counter(train_labels)
min_count = min(label_counts.values())

if min_count < 2:
    print(f"Warning: Minimum class count is {min_count}, falling back to random sampling for train/val split")
    indices = np.arange(len(train_files))
    np.random.shuffle(indices)
    train_idx, val_idx = train_test_split(
        indices,
        test_size=0.2,
        random_state=42,
    )
else:
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
        return img, self.labels[idx]

# ---------- Transforms ----------
transform_train = T.Compose([
    T.Resize((224, 224)),
    T.RandomHorizontalFlip(p=0.5),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

transform_val = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# ---------- DataLoaders ----------
train_dataset = ImgDataset(train_files_split, train_labels_split, transform=transform_train)
val_dataset = ImgDataset(val_files_split, val_labels_split, transform=transform_val)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=0)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=0)

# ---------- Model ----------
model = models.mobilenet_v2(pretrained=True)
model.classifier[1] = nn.Linear(model.last_channel, num_classes)

# Freeze backbone
for param in model.features.parameters():
    param.requires_grad = False

# ---------- Training Setup ----------
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.classifier.parameters(), lr=0.001)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# ---------- Training Loop ----------
num_epochs = 5
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for inputs, labels in tqdm(train_loader):
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}")

# ---------- Validation ----------
model.eval()
all_preds = []
all_labels = []
with torch.no_grad():
    for inputs, labels in val_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        _, preds = torch.max(outputs, 1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

accuracy = accuracy_score(all_labels, all_preds)
print(f"Validation Accuracy: {accuracy:.4f}")