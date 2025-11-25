import os
import json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import tifffile
import cv2
from sklearn.model_selection import KFold
import timm
from segmentation_models_pytorch import Unet
from segmentation_models_pytorch.losses import DiceLoss
from torch.optim import AdamW
import albumentations as A
from albumentations.pytorch import ToTensorV2

# Define constants
DATA_DIR = "./data"
TRAIN_DIR = os.path.join(DATA_DIR, "train")
TEST_DIR = os.path.join(DATA_DIR, "test")
IMAGE_SIZE = 512


# Define dataset class
class HuBMAPDataset(Dataset):
    def __init__(self, image_paths, mask_paths, transform=None):
        self.image_paths = image_paths
        self.mask_paths = mask_paths
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        mask_path = self.mask_paths[idx]

        image = tifffile.imread(image_path)
        mask = self.load_mask(mask_path, image.shape[:2])

        if self.transform:
            augmented = self.transform(image=image, mask=mask)
            image = augmented["image"]
            mask = augmented["mask"]

        return image, mask

    def load_mask(self, json_path, image_shape):
        with open(json_path, "r") as f:
            annotations = json.load(f)

        mask = np.zeros(image_shape, dtype=np.uint8)
        for annotation in annotations:
            coords = np.array(annotation["geometry"]["coordinates"][0])
            coords = coords.astype(np.int32)
            coords = coords.reshape((-1, 1, 2))
            cv2.fillPoly(mask, [coords], 1)

        return mask


# Define data augmentation
def get_train_transform():
    return A.Compose(
        [
            A.Resize(IMAGE_SIZE, IMAGE_SIZE),
            A.Normalize(),
            ToTensorV2(),
        ]
    )


def get_val_transform():
    return A.Compose(
        [
            A.Resize(IMAGE_SIZE, IMAGE_SIZE),
            A.Normalize(),
            ToTensorV2(),
        ]
    )


# Define model
class SwinUnet(nn.Module):
    def __init__(self):
        super(SwinUnet, self).__init__()
        self.encoder = timm.create_model(
            "swin_tiny_patch4_window7_224", pretrained=True, features_only=True
        )
        self.decoder = Unet(
            encoder_name="swin_tiny_patch4_window7_224", classes=1, activation=None
        )

    def forward(self, x):
        features = self.encoder(x)
        outputs = self.decoder(x)
        return outputs


# Define training function
def train(model, device, loader, criterion, optimizer):
    model.train()
    total_loss = 0
    for images, masks in loader:
        images, masks = images.to(device), masks.to(device).float().unsqueeze(1)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, masks)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(loader)


# Define evaluation function
def evaluate(model, device, loader, criterion):
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for images, masks in loader:
            images, masks = images.to(device), masks.to(device).float().unsqueeze(1)
            outputs = model(images)
            loss = criterion(outputs, masks)
            total_loss += loss.item()
    return total_loss / len(loader)


# Define main function
def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load data
    train_df = pd.read_csv(os.path.join(DATA_DIR, "train.csv"))
    train_image_paths = [
        os.path.join(TRAIN_DIR, f"{image_id}.tiff") for image_id in train_df["id"]
    ]
    train_mask_paths = [
        os.path.join(TRAIN_DIR, f"{image_id}.json") for image_id in train_df["id"]
    ]

    test_image_paths = [
        os.path.join(TEST_DIR, file)
        for file in os.listdir(TEST_DIR)
        if file.endswith(".tiff")
    ]

    # Define 5-fold cross-validation
    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    # Define model, criterion, and optimizer
    model = SwinUnet().to(device)
    criterion = DiceLoss(mode="binary")
    optimizer = AdamW(model.parameters(), lr=1e-4)

    # Perform 5-fold cross-validation
    dice_scores = []
    for fold, (train_idx, val_idx) in enumerate(kf.split(train_image_paths)):
        train_dataset = HuBMAPDataset(
            [train_image_paths[i] for i in train_idx],
            [train_mask_paths[i] for i in train_idx],
            transform=get_train_transform(),
        )
        val_dataset = HuBMAPDataset(
            [train_image_paths[i] for i in val_idx],
            [train_mask_paths[i] for i in val_idx],
            transform=get_val_transform(),
        )

        train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=4, shuffle=False)

        for epoch in range(10):
            train_loss = train(model, device, train_loader, criterion, optimizer)
            val_loss = evaluate(model, device, val_loader, criterion)
            print(
                f"Fold {fold+1}, Epoch {epoch+1}, Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}"
            )

        # Evaluate Dice score on validation set
        model.eval()
        dice_score = 0
        with torch.no_grad():
            for images, masks in val_loader:
                images, masks = images.to(device), masks.to(device).float().unsqueeze(1)
                outputs = model(images)
                dice_score += criterion(outputs, masks).item()
        dice_score /= len(val_loader)
        dice_scores.append(1 - dice_score)
        print(f"Fold {fold+1}, Dice Score: {dice_scores[-1]:.4f}")

    # Print average Dice score
    print(f"Average Dice Score: {np.mean(dice_scores):.4f}")

    # Make predictions on test data
    test_dataset = HuBMAPDataset(
        test_image_paths, [None] * len(test_image_paths), transform=get_val_transform()
    )
    test_loader = DataLoader(test_dataset, batch_size=4, shuffle=False)

    model.eval()
    predictions = []
    with torch.no_grad():
        for images, _ in test_loader:
            images = images.to(device)
            outputs = model(images)
            predictions.extend(torch.sigmoid(outputs).cpu().numpy())

    # Save predictions to submission file
    submission_df = pd.DataFrame(
        {
            "id": [
                file.split(".")[0]
                for file in os.listdir(TEST_DIR)
                if file.endswith(".tiff")
            ],
            "predicted": predictions,
        }
    )
    submission_df.to_csv("submission.csv", index=False)


if __name__ == "__main__":
    main()
