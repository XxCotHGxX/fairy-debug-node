import os
import sys
import zipfile
import pandas as pd
import numpy as np
from pathlib import Path

# ==========================================
# FAIRY DEBUGGER TEMPLATE
# ==========================================

# 1. SETUP PATHS
# The competition data is mounted at /root/data (READ-ONLY)
# We must extract any compressed files to the current directory (WRITABLE)
DATA_DIR = Path("/root/data") if os.path.exists("/root/data") else Path("./data")
WORK_DIR = Path(".")

print(f"Data Directory: {DATA_DIR}")
print(f"Work Directory: {WORK_DIR}")

# 2. DATA EXTRACTION HELPER
def extract_data(zip_name, target_dir=None):
    """
    Extracts a zip file from DATA_DIR to WORK_DIR.
    Handles the case where the zip might already be extracted.
    """
    zip_path = DATA_DIR / zip_name
    
    # If target_dir is not specified, determine it from the zip structure or name
    # But for safety, we often extract to a folder named after the zip
    if target_dir is None:
        target_dir = zip_name.replace('.zip', '').replace('.7z', '')
        
    extract_path = WORK_DIR / target_dir
    
    if extract_path.exists():
        print(f"Directory {extract_path} already exists. Skipping extraction.")
        return extract_path
        
    if not zip_path.exists():
        print(f"Warning: Zip file {zip_path} not found.")
        return None

    print(f"Extracting {zip_path} to {extract_path}...")
    try:
        if zip_name.endswith('.zip'):
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(extract_path)
        elif zip_name.endswith('.7z'):
            # Handle 7z if needed (requires py7zr)
            try:
                import py7zr
                with py7zr.SevenZipFile(zip_path, mode='r') as z:
                    z.extractall(path=extract_path)
            except ImportError:
                print("py7zr not installed. Please install it if you need to extract .7z files.")
                # Fallback or error
        print("Extraction complete.")
    except Exception as e:
        print(f"Error extracting {zip_name}: {e}")
        
    return extract_path

# 3. COMPETITION SPECIFIC SETUP
# TODO: Update these filenames for your specific competition
# Example:
# train_path = extract_data("train.zip")
# test_path = extract_data("test.zip")

# 4. YOUR CODE HERE
def main():
    print("Starting job...")
    
    # Example: Loading a CSV
    # df = pd.read_csv(DATA_DIR / "train.csv")
    # print(df.head())
    
    # TODO: Implement your training/inference logic here
    
    # 5. SAVE SUBMISSION
    # Must save to ./submission.csv
    print("Saving submission...")
    # submission_df.to_csv("submission.csv", index=False)
    print("Done!")

if __name__ == "__main__":
    main()
