#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold

# ---------------------------------------------------------
# 1. Helper functions
# ---------------------------------------------------------


def ecef_to_latlon(x, y, z):
    """Convert ECEF (meters) to latitude/longitude (degrees) using WGS‑84."""
    a = 6378137.0  # semi‑major axis
    e2 = 6.69437999014e-3  # first eccentricity squared

    b = np.sqrt(a**2 * (1 - e2))
    ep = np.sqrt((a**2 - b**2) / b**2)

    p = np.sqrt(x**2 + y**2)
    th = np.arctan2(a * z, b * p)

    lon = np.arctan2(y, x)
    lat = np.arctan2(z + ep**2 * b * np.sin(th) ** 3, p - e2 * a * np.cos(th) ** 3)

    lat = np.degrees(lat)
    lon = np.degrees(lon)
    lon = (lon + 360) % 360  # normalise to [0,360)

    return lat, lon


def haversine_m(lat1, lon1, lat2, lon2):
    """Vectorised haversine distance in metres."""
    R = 6371000.0  # Earth radius in metres
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c


def compute_phone_metric(df):
    """Mean of 50th and 95th percentile distance errors for one phone."""
    df = df.dropna(
        subset=["LatitudeDegrees", "LongitudeDegrees", "pred_lat", "pred_lon"]
    )
    if df.empty:
        return np.nan
    d = haversine_m(
        df["LatitudeDegrees"].values,
        df["LongitudeDegrees"].values,
        df["pred_lat"].values,
        df["pred_lon"].values,
    )
    if d.size == 0:
        return np.nan
    p50 = np.percentile(d, 50)
    p95 = np.percentile(d, 95)
    return (p50 + p95) / 2.0


# ---------------------------------------------------------
# 2. Load training data
# ---------------------------------------------------------


def build_train_dataframe(root="./data/train"):
    rows = []
    for drive_path in sorted(glob.glob(os.path.join(root, "*/*"))):
        if not os.path.isdir(drive_path):
            continue
        drive_id = os.path.basename(os.path.dirname(drive_path))
        phone_name = os.path.basename(drive_path)
        phone_id = f"{drive_id}/{phone_name}"

        gt_path = os.path.join(drive_path, "ground_truth.csv")
        if not os.path.exists(gt_path):
            continue
        gt = pd.read_csv(
            gt_path, usecols=["UnixTimeMillis", "LatitudeDegrees", "LongitudeDegrees"]
        )
        gt.rename(columns={"UnixTimeMillis": "timestamp"}, inplace=True)

        gnss_path = os.path.join(drive_path, "device_gnss.csv")
        gnss = pd.read_csv(
            gnss_path,
            usecols=[
                "utcTimeMillis",
                "WlsPositionXEcefMeters",
                "WlsPositionYEcefMeters",
                "WlsPositionZEcefMeters",
            ],
        )
        gnss.rename(columns={"utcTimeMillis": "timestamp"}, inplace=True)

        merged = pd.merge(gt, gnss, on="timestamp", how="inner")
        if merged.empty:
            continue

        lat_pred, lon_pred = ecef_to_latlon(
            merged["WlsPositionXEcefMeters"].values,
            merged["WlsPositionYEcefMeters"].values,
            merged["WlsPositionZEcefMeters"].values,
        )
        merged["pred_lat"] = lat_pred
        merged["pred_lon"] = lon_pred
        merged["phone_id"] = phone_id

        rows.append(
            merged[
                [
                    "phone_id",
                    "timestamp",
                    "LatitudeDegrees",
                    "LongitudeDegrees",
                    "pred_lat",
                    "pred_lon",
                ]
            ]
        )
    if not rows:
        raise RuntimeError("No training data found!")
    return pd.concat(rows, ignore_index=True)


train_df = build_train_dataframe()
print(f"Loaded training rows: {len(train_df)}")
unique_phones = train_df["phone_id"].unique()
print(f"Unique phones: {len(unique_phones)}")


# ---------------------------------------------------------
# 3. 5‑fold CV (no model)
# ---------------------------------------------------------

kf = KFold(n_splits=5, shuffle=True, random_state=42)
fold_scores = []

for fold_idx, (train_idx, val_idx) in enumerate(kf.split(unique_phones), 1):
    val_phones = unique_phones[val_idx]
    val_mask = train_df["phone_id"].isin(val_phones)
    val_data = train_df[val_mask]

    phone_metrics = [compute_phone_metric(g) for _, g in val_data.groupby("phone_id")]
    fold_score = np.nanmean(phone_metrics) if phone_metrics else np.nan
    print(f"Fold {fold_idx} score: {fold_score:.4f} m")
    fold_scores.append(fold_score)

cv_score = np.nanmean(fold_scores)
print(f"\n5‑fold CV mean score: {cv_score:.4f} metres")


# ---------------------------------------------------------
# 4. Generate submission for the test set
# ---------------------------------------------------------


def build_test_predictions(
    root="./data/test",
    sample_path="./data/sample_submission.csv",
    out_path="./submission.csv",
):
    # Load the required rows template
    sample_sub = pd.read_csv(
        sample_path, dtype={"phone": str, "UnixTimeMillis": np.int64}
    )

    # Bug Fix: Normalize column names (tripId -> phone)
    if "phone" not in sample_sub.columns and "tripId" in sample_sub.columns:
        sample_sub.rename(columns={"tripId": "phone"}, inplace=True)

    # We'll build a lookup DataFrame with predictions for every GNSS timestamp
    pred_rows = []
    for drive_path in sorted(glob.glob(os.path.join(root, "*/*"))):
        if not os.path.isdir(drive_path):
            continue
        drive_id = os.path.basename(os.path.dirname(drive_path))
        phone_name = os.path.basename(drive_path)
        phone_id = f"{drive_id}/{phone_name}"  # matches the format used in sample

        gnss_path = os.path.join(drive_path, "device_gnss.csv")
        if not os.path.exists(gnss_path):
            continue
        gnss = pd.read_csv(
            gnss_path,
            usecols=[
                "utcTimeMillis",
                "WlsPositionXEcefMeters",
                "WlsPositionYEcefMeters",
                "WlsPositionZEcefMeters",
            ],
        )
        lat_pred, lon_pred = ecef_to_latlon(
            gnss["WlsPositionXEcefMeters"].values,
            gnss["WlsPositionYEcefMeters"].values,
            gnss["WlsPositionZEcefMeters"].values,
        )
        pred_rows.append(
            pd.DataFrame(
                {
                    "phone": phone_id,
                    "UnixTimeMillis": gnss["utcTimeMillis"],
                    "LatitudeDegrees": lat_pred,
                    "LongitudeDegrees": lon_pred,
                }
            )
        )

    if not pred_rows:
        raise RuntimeError("No test data found!")
    all_preds = pd.concat(pred_rows, ignore_index=True)

    # Keep only rows present in the sample submission, preserving its order
    submission = pd.merge(
        sample_sub,
        all_preds,
        on=["phone", "UnixTimeMillis"],
        how="left",
        suffixes=("", "_pred"),
    )
    # In rare cases a timestamp may be missing; fill with NaN (Kaggle will treat as missing)
    submission = submission[
        ["phone", "UnixTimeMillis", "LatitudeDegrees", "LongitudeDegrees"]
    ]
    
    # Interpolate missing values to ensure valid submission
    submission = submission.interpolate(method='linear', limit_direction='both')

    # Bug Fix: Rename 'phone' back to 'tripId' to match competition format
    submission.rename(columns={"phone": "tripId"}, inplace=True)

    submission.to_csv(out_path, index=False)
    print(f"Submission written to {out_path} – rows: {len(submission)}")


build_test_predictions()

# ---------------------------------------------------------
# End of script
# ---------------------------------------------------------
