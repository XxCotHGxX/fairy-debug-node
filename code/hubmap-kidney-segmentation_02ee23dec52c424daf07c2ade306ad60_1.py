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
        #self.encoder = timm.create_model(
        #    "swin_tiny_patch4_window7_224", pretrained=True, features_only=True
        #)
        self.decoder = Unet(
            encoder_name="resnet34", classes=1, activation=None
        )

    def forward(self, x):
        #features = self.encoder(x)
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
        os.path.join(TEST_DIR, f"{image_id}.tiff") for image_id in train_df["id"]
    ]