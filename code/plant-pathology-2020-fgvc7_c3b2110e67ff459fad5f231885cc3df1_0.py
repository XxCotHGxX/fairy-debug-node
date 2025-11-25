# --------------------------------------------------------------
#  Plant Pathology Challenge – Fixed End‑to‑End Solution
# --------------------------------------------------------------

# 1. Disable HF offline mode before any library import
import os

if "HF_HUB_OFFLINE" in os.environ:
    del os.environ["HF_HUB_OFFLINE"]

# Standard imports
import gc
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.metrics import roc_auc_score
from iterstrat.ml_stratifiers import MultilabelStratifiedKFold

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torch.cuda.amp import autocast, GradScaler

import albumentations as A
from albumentations.pytorch import ToTensorV2
import timm
from PIL import Image  # proper image loader

# --------------------------- Config --------------------------- #
SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)

IMG_DIR = "./data/images"
TRAIN_CSV = "./data/train.csv"
TEST_CSV = "./data/test.csv"
SUBMIT_PATH = "./submission.csv"

BATCH_SIZE = 32
IMG_SIZE = 224
N_EPOCHS = 6
N_FOLDS = 5
LR = 1e-4
WEIGHT_DECAY = 1e-5
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# --------------------------- Dataset --------------------------- #
class PlantDataset(Dataset):
    def __init__(self, df, is_train=True, transforms=None):
        self.df = df.reset_index(drop=True)
        self.is_train = is_train
        self.transforms = transforms

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img_path = os.path.join(IMG_DIR, f"{row['image_id']}.jpg")
        # Load image with PIL, convert to numpy array for albumentations
        image = np.array(Image.open(img_path).convert("RGB"))

        if self.transforms:
            image = self.transforms(image=image)["image"]

        if self.is_train:
            targets = row[
                ["multiple_diseases", "healthy", "rust", "scab"]
            ].values.astype(np.float32)
            return image, torch.tensor(targets)
        else:
            # For test set we only need the id
            return image, row["image_id"]


def get_train_transforms():
    return A.Compose(
        [
            A.RandomResizedCrop(IMG_SIZE, IMG_SIZE, scale=(0.8, 1.0)),
            A.HorizontalFlip(),
            A.VerticalFlip(),
            A.RandomRotate90(),
            A.Transpose(),
            A.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
            A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            ToTensorV2(),
        ]
    )


def get_valid_transforms():
    return A.Compose(
        [
            A.Resize(IMG_SIZE, IMG_SIZE),
            A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            ToTensorV2(),
        ]
    )


# --------------------------- Model Wrapper --------------------------- #
class MultiLabelModel(nn.Module):
    def __init__(self, backbone_name):
        super().__init__()
        # Use pretrained=False to avoid offline download issues
        self.backbone = timm.create_model(
            backbone_name, pretrained=False, num_classes=0
        )
        backbone_out = self.backbone.num_features
        self.head = nn.Linear(backbone_out, 4)

    def forward(self, x):
        feat = self.backbone(x)
        logits = self.head(feat)
        return logits


# --------------------------- Training Utils --------------------------- #
def train_one_epoch(model, loader, optimizer, criterion, scaler):
    model.train()
    epoch_loss = 0.0
    for img, tgt in loader:
        img = img.to(DEVICE, non_blocking=True)
        tgt = tgt.to(DEVICE, non_blocking=True)

        optimizer.zero_grad()
        with autocast():
            logits = model(img)
            loss = criterion(logits, tgt)
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        epoch_loss += loss.item() * img.size(0)
    return epoch_loss / len(loader.dataset)


def validate(model, loader):
    model.eval()
    preds = []
    trues = []
    with torch.no_grad():
        for img, tgt in loader:
            img = img.to(DEVICE, non_blocking=True)
            logits = model(img)
            probs = torch.sigmoid(logits).cpu().numpy()
            preds.append(probs)
            trues.append(tgt.numpy())
    preds = np.concatenate(preds)
    trues = np.concatenate(trues)

    aucs = []
    for i in range(trues.shape[1]):
        try:
            auc = roc_auc_score(trues[:, i], preds[:, i])
        except ValueError:
            auc = np.nan
        aucs.append(auc)
    mean_auc = np.nanmean(aucs)
    return mean_auc, preds, trues


def fit_model(model, train_df, valid_df):
    train_ds = PlantDataset(train_df, is_train=True, transforms=get_train_transforms())
    valid_ds = PlantDataset(valid_df, is_train=True, transforms=get_valid_transforms())

    train_loader = DataLoader(
        train_ds,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=4,
        pin_memory=True,
        drop_last=True,
    )
    valid_loader = DataLoader(
        valid_ds,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=4,
        pin_memory=True,
    )

    model = model.to(DEVICE)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=N_EPOCHS)
    scaler = GradScaler()

    best_auc = 0.0
    best_state = None
    for epoch in range(N_EPOCHS):
        train_one_epoch(model, train_loader, optimizer, criterion, scaler)
        scheduler.step()
        val_auc, _, _ = validate(model, valid_loader)
        if val_auc > best_auc:
            best_auc = val_auc
            best_state = model.state_dict()
    if best_state is not None:
        model.load_state_dict(best_state)
    return model, best_auc


# --------------------------- Main Pipeline --------------------------- #
def main():
    # Load data
    train_df = pd.read_csv(TRAIN_CSV)
    test_df = pd.read_csv(TEST_CSV)

    # Stratified K-Fold setup
    y = train_df[["multiple_diseases", "healthy", "rust", "scab"]].values
    mskf = MultilabelStratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)

    cv_scores = []
    oof_preds = np.zeros((len(train_df), 4))

    for fold, (tr_idx, val_idx) in enumerate(mskf.split(train_df, y)):
        print(f"\n=== Fold {fold + 1}/{N_FOLDS} ===")
        tr_df = train_df.iloc[tr_idx].reset_index(drop=True)
        val_df = train_df.iloc[val_idx].reset_index(drop=True)

        # Model A: ConvNeXt
        model_a = MultiLabelModel("convnext_base")
        model_a, _ = fit_model(model_a, tr_df, val_df)

        # Model B: Swin Transformer
        model_b = MultiLabelModel("swin_base_patch4_window7_224")
        model_b, _ = fit_model(model_b, tr_df, val_df)

        # Validation ensemble
        val_ds = PlantDataset(val_df, is_train=True, transforms=get_valid_transforms())
        val_loader = DataLoader(
            val_ds,
            batch_size=BATCH_SIZE,
            shuffle=False,
            num_workers=4,
            pin_memory=True,
        )

        preds_a, preds_b = [], []
        model_a.eval()
        model_b.eval()
        with torch.no_grad():
            for img, _ in val_loader:
                img = img.to(DEVICE)
                with autocast():
                    logits_a = model_a(img)
                    logits_b = model_b(img)
                probs_a = torch.sigmoid(logits_a).cpu().numpy()
                probs_b = torch.sigmoid(logits_b).cpu().numpy()
                preds_a.append(probs_a)
                preds_b.append(probs_b)

        preds_a = np.concatenate(preds_a)
        preds_b = np.concatenate(preds_b)
        ensemble_pred = (preds_a + preds_b) / 2.0

        # Compute fold AUC
        fold_aucs = []
        for i in range(4):
            try:
                auc = roc_auc_score(val_df.iloc[:, i + 1].values, ensemble_pred[:, i])
            except ValueError:
                auc = np.nan
            fold_aucs.append(auc)
        fold_mean = np.nanmean(fold_aucs)
        print(f"Fold {fold + 1} mean ROC‑AUC: {fold_mean:.5f}")
        cv_scores.append(fold_mean)
        oof_preds[val_idx] = ensemble_pred

        # Clean up
        del model_a, model_b, tr_df, val_df
        gc.collect()
        torch.cuda.empty_cache()

    print("\n=== CV Summary ===")
    print(f"Mean CV AUC: {np.mean(cv_scores):.5f}  Std: {np.std(cv_scores):.5f}")

    # ---------------- Train final models on full data ---------------- #
    print("\nTraining final models on full data...")
    model_a_full = MultiLabelModel("convnext_base")
    model_a_full, _ = fit_model(model_a_full, train_df, train_df)

    model_b_full = MultiLabelModel("swin_base_patch4_window7_224")
    model_b_full, _ = fit_model(model_b_full, train_df, train_df)

    # ---------------- Predict on test set ---------------- #
    test_ds = PlantDataset(test_df, is_train=False, transforms=get_valid_transforms())
    test_loader = DataLoader(
        test_ds,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=4,
        pin_memory=True,
    )

    test_preds_a, test_preds_b = [], []
    ids = []
    model_a_full.eval()
    model_b_full.eval()
    with torch.no_grad():
        for img, img_id in tqdm(test_loader, desc="Predict test"):
            img = img.to(DEVICE)
            ids.extend(img_id)  # img_id is a list of strings
            with autocast():
                logits_a = model_a_full(img)
                logits_b = model_b_full(img)
            probs_a = torch.sigmoid(logits_a).cpu().numpy()
            probs_b = torch.sigmoid(logits_b).cpu().numpy()
            test_preds_a.append(probs_a)
            test_preds_b.append(probs_b)

    test_preds_a = np.concatenate(test_preds_a)
    test_preds_b = np.concatenate(test_preds_b)
    test_pred = (test_preds_a + test_preds_b) / 2.0

    # ------------------- Save submission ------------------- #
    submission = pd.DataFrame(
        {
            "image_id": ids,
            "multiple_diseases": test_pred[:, 0],
            "healthy": test_pred[:, 1],
            "rust": test_pred[:, 2],
            "scab": test_pred[:, 3],
        }
    )
    submission.to_csv(SUBMIT_PATH, index=False)
    print(f"\nSubmission saved to {SUBMIT_PATH}")


if __name__ == "__main__":
    main()
