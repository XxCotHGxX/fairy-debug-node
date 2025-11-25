================================================================================
MLE-BENCH DATA EXTRACTION ISSUE - COMPREHENSIVE GUIDE
================================================================================

PROBLEM OVERVIEW:
-----------------
MLE-bench buggy code frequently fails with FileNotFoundError, ValueError, or
OSError when trying to access dataset files. The root cause is that competition
data is provided in a READ-ONLY ./data directory (mounted from MLE_BENCH_DATA_DIR),
often as ZIP archives that must be extracted to a WRITABLE directory before use.

ENVIRONMENT SETUP:
------------------
- ./data = READ-ONLY directory containing competition files (ZIPs, CSVs)
  - Mounted from: MLE_BENCH_DATA_DIR in .env (e.g., ~/.cache/mle-bench/data/)
  - Location in container: bound to /root/data (read-only)
  - Contains: train.zip, test.zip, train.csv, sample_submission.csv, etc.
  - CRITICAL: YOU CANNOT WRITE TO THIS DIRECTORY - EVER
  - ANY attempt to extract/write to ./data will cause OSError [Errno 30] Read-only file system

- . (current working directory) = WRITABLE directory for extracted files
  - The current working directory is ALWAYS writable
  - Extract ZIP files to "." NOT to "./data"
  - For simple cases, use EXTRACT_DIR = "." as the extraction target

COMMON ERROR PATTERNS:
----------------------
1. FileNotFoundError: [Errno 2] No such file or directory: './data/train/image.jpg'
   - Cause: Code tries to read from unextracted ZIP
   - Solution: Extract ZIP first

2. FileNotFoundError: [Errno 2] No such file or directory: './data/train.json'
   - Cause: Code tries to read train.json, but actual file is train.json.7z
   - Solution: Extract 7z file first using py7zr

3. ValueError: need at least one array to stack
   - Cause: File list is empty because data not extracted
   - Solution: Extract ZIP, then list files

4. OSError: [Errno 30] Read-only file system
   - Cause: Code tries to write to ./data directory
   - Solution: Write to ./extracted_data instead

5. ModuleNotFoundError: No module named 'py7zr'
   - Cause: Code tries to import py7zr but it's not installed
   - Solution: Add try/except block with pip install before importing

THE CRITICAL ZIP STRUCTURE ISSUE:
----------------------------------
ZIP files can have two different internal structures:

CASE A: Files at root level (NO internal subdirectory)
  train.zip contains:
    image1.jpg
    image2.jpg
    ...

  CORRECT extraction:
    z.extractall(os.path.join(work_dir, "train"))

  Result: ./extracted_data/train/image1.jpg

  WRONG extraction:
    z.extractall(work_dir)

  Result: ./extracted_data/image1.jpg
  (Code expects ./extracted_data/train/image1.jpg)

CASE B: Files in subdirectory (HAS internal subdirectory)
  train2.zip contains:
    train2/audio1.aif
    train2/audio2.aif
    ...

  CORRECT extraction:
    z.extractall(work_dir)

  Result: ./extracted_data/train2/audio1.aif

  WRONG extraction:
    z.extractall(os.path.join(work_dir, "train2"))

  Result: ./extracted_data/train2/train2/audio1.aif

RECOMMENDED SOLUTION PATTERN:
-----------------------------
Always add this block BEFORE any file path definitions:

```python
import os
import zipfile

# Define directories
DATA_DIR = "./data"  # Read-only source
work_dir = "./extracted_data"  # Writable destination

# Create writable directory
os.makedirs(work_dir, exist_ok=True)

# Extract train data
train_zip = os.path.join(DATA_DIR, "train.zip")
if os.path.exists(train_zip):
    # Check ZIP structure first
    with zipfile.ZipFile(train_zip, "r") as z:
        namelist = z.namelist()
        # If files are at root level (no common subdirectory)
        if not any("/" in name for name in namelist[:5]):
            # Extract to train/ subdirectory
            target_dir = os.path.join(work_dir, "train")
            if not os.path.exists(target_dir):
                z.extractall(target_dir)
        else:
            # Extract normally (preserves internal structure)
            if not os.path.exists(os.path.join(work_dir, "train")):
                z.extractall(work_dir)

# Similar for test.zip
test_zip = os.path.join(DATA_DIR, "test.zip")
# ... repeat pattern above ...
```

ALTERNATIVE: INSPECT THEN DECIDE
---------------------------------
For maximum robustness, use recursive file finding after extraction:

```python
import glob

# Extract ZIPs to work_dir
os.makedirs(work_dir, exist_ok=True)

if os.path.exists(train_zip):
    with zipfile.ZipFile(train_zip, "r") as z:
        z.extractall(work_dir)

# Find files recursively (handles any structure)
def find_files(base_dir, extension):
    pattern = os.path.join(base_dir, "**", f"*.{extension}")
    return sorted(glob.glob(pattern, recursive=True))

train_files = find_files(work_dir, "jpg")
```

CSV FILES:
----------
CSVs can appear in two forms:

1. UNCOMPRESSED CSVs (train.csv, sample_submission.csv) can be read DIRECTLY from
   ./data without extraction:
   ```python
   TRAIN_CSV = os.path.join(DATA_DIR, "train.csv")  # Read from ./data
   TEST_CSV = os.path.join(DATA_DIR, "sample_submission.csv")  # Read from ./data
   ```

2. COMPRESSED CSVs (train.csv.zip, test.csv.zip) MUST be extracted FIRST:

   WRONG APPROACH (causes OSError [Errno 30]):
   ```python
   DATA_DIR = "./data"
   TRAIN_ZIP = os.path.join(DATA_DIR, "ru_train.csv.zip")
   with zipfile.ZipFile(TRAIN_ZIP, 'r') as z:
       z.extractall(DATA_DIR)  # FAILS - ./data is read-only!
   ```

   CORRECT APPROACH (extract to current directory):
   ```python
   DATA_DIR = "./data"
   EXTRACT_DIR = "."  # Current directory is writable

   TRAIN_ZIP = os.path.join(DATA_DIR, "ru_train.csv.zip")
   TRAIN_CSV = os.path.join(EXTRACT_DIR, "ru_train.csv")

   if os.path.exists(TRAIN_ZIP) and not os.path.exists(TRAIN_CSV):
       with zipfile.ZipFile(TRAIN_ZIP, 'r') as z:
           z.extractall(EXTRACT_DIR)  # Extract to current directory

   # Now read from EXTRACT_DIR, not DATA_DIR
   train_df = pd.read_csv(TRAIN_CSV)
   ```

7Z FILES (.7z archives):
-------------------------
Some datasets use 7z compression instead of ZIP. These files have .7z extension
(e.g., train.json.7z, test.json.7z) and require the py7zr library to extract.

COMMON ERROR PATTERN:
   FileNotFoundError: [Errno 2] No such file or directory: './data/train.json'
   - Cause: Code tries to read train.json, but actual file is train.json.7z
   - Solution: Extract .7z file first using py7zr

SOLUTION PATTERN (self-contained with pip install):
   ```python
   import subprocess
   from pathlib import Path

   # Install py7zr if not available (self-contained approach)
   try:
       import py7zr
   except ImportError:
       subprocess.run(['pip', 'install', 'py7zr'], check=True)
       import py7zr

   DATA_PATH = Path("./data")
   TRAIN_FILE = Path("./train.json")
   TEST_FILE = Path("./test.json")

   # Extract 7z files if needed
   TRAIN_7Z = DATA_PATH / "train.json.7z"
   TEST_7Z = DATA_PATH / "test.json.7z"

   if TRAIN_7Z.exists() and not TRAIN_FILE.exists():
       with py7zr.SevenZipFile(TRAIN_7Z, mode='r') as z:
           z.extractall(path=".")

   if TEST_7Z.exists() and not TEST_FILE.exists():
       with py7zr.SevenZipFile(TEST_7Z, mode='r') as z:
           z.extractall(path=".")

   # Now load the extracted files
   with open(TRAIN_FILE, 'r') as f:
       train_data = json.load(f)
   ```

KEY POINTS FOR 7Z FILES:
   1. py7zr is NOT in the standard library - use try/except to install it
   2. Extract to current directory "." (writable), NOT to ./data (read-only)
   3. Update file paths to point to current directory, not ./data
   4. Use SevenZipFile.extractall(path=".") to extract to current directory
   5. Check if extracted file exists before re-extracting (avoid redundant work)

COMPLETE EXAMPLE (aerial-cactus-identification):
-------------------------------------------------
```python
import os
import zipfile

DATA_DIR = "./data"
train_zip = os.path.join(DATA_DIR, "train.zip")
test_zip = os.path.join(DATA_DIR, "test.zip")
work_dir = "./extracted_data"

os.makedirs(work_dir, exist_ok=True)

# train.zip has files at root, extract TO train/ directory
if os.path.exists(train_zip) and not os.path.exists(os.path.join(work_dir, "train")):
    with zipfile.ZipFile(train_zip, "r") as z:
        z.extractall(os.path.join(work_dir, "train"))

# test.zip has files at root, extract TO test/ directory
if os.path.exists(test_zip) and not os.path.exists(os.path.join(work_dir, "test")):
    with zipfile.ZipFile(test_zip, "r") as z:
        z.extractall(os.path.join(work_dir, "test"))

# Set paths
TRAIN_IMG_DIR = os.path.join(work_dir, "train")
TEST_IMG_DIR = os.path.join(work_dir, "test")
TRAIN_CSV = os.path.join(DATA_DIR, "train.csv")  # Read from ./data
TEST_CSV = os.path.join(DATA_DIR, "sample_submission.csv")  # Read from ./data
```

DEBUGGING CHECKLIST:
--------------------
When encountering FileNotFoundError:

1. Check if ZIPs or 7z files exist:
   ls -la ./data/*.zip
   ls -la ./data/*.7z

2. Inspect ZIP contents:
   unzip -l ./data/train.zip | head -20

   For 7z files:
   7z l ./data/train.json.7z

3. Check if extraction happened:
   ls -la ./extracted_data/
   ls -la ./*.json

4. Verify expected file paths:
   - Print img_path in __getitem__ before opening
   - Check if file actually exists at that path

5. Check ZIP internal structure:
   - No "/" in first few entries = files at root level
   - Has "/" in entries = has subdirectories

COMMON MISTAKES TO AVOID:
-------------------------
1. DON'T extract to ./data (read-only) - THIS IS THE MOST COMMON ERROR
   - ALWAYS extract to "." (current directory) or "./extracted_data"
   - NEVER use extractall(DATA_DIR) when DATA_DIR = "./data"
   - If you see OSError [Errno 30] Read-only file system, you extracted to ./data
2. DON'T assume ZIP structure without checking
3. DON'T use relative paths like "../data"
4. DON'T forget to import zipfile (or py7zr for .7z files)
5. DON'T extract multiple times (check if already extracted)
6. DON'T hardcode paths - use os.path.join()
7. DON'T read extracted files from ./data - read from EXTRACT_DIR instead
8. DON'T assume py7zr is installed - add try/except with pip install for 7z files

BATCH SIZE CONSIDERATION:
-------------------------
Often need to reduce BATCH_SIZE from default (e.g., 256 -> 64) due to GPU
memory constraints, especially with Vision Transformers or large models.

REFERENCE EXAMPLES:
-------------------
- buggy_code_131.py (aerial-cactus-identification): Case A - files at root
- buggy_code_132.py (whale-detection): Case B - files in subdirectory
- buggy_code_140_3.py (text-normalization-russian): CSV ZIPs extracted to current dir
- statoil-iceberg-classifier-challenge: 7z files requiring py7zr library

SPECIFIC DATASET PATTERNS:
--------------------------
text-normalization-challenge-russian-language:
  - Data files: ru_train.csv.zip, ru_test_2.csv.zip in ./data/
  - These are CSV files inside ZIPs, NOT image directories
  - MUST extract to current directory: EXTRACT_DIR = "."
  - Pattern:
    ```python
    DATA_PATH = "./data"
    EXTRACT_DIR = "."
    TRAIN_ZIP = os.path.join(DATA_PATH, "ru_train.csv.zip")
    TEST_ZIP = os.path.join(DATA_PATH, "ru_test_2.csv.zip")
    TRAIN_FILE = os.path.join(EXTRACT_DIR, "ru_train.csv")
    TEST_FILE = os.path.join(EXTRACT_DIR, "ru_test_2.csv")

    # Extract to current directory
    if os.path.exists(TRAIN_ZIP) and not os.path.exists(TRAIN_FILE):
        with zipfile.ZipFile(TRAIN_ZIP, 'r') as z:
            z.extractall(EXTRACT_DIR)
    ```

iwildcam-2019-fgvc6:
  - Data files: train_images.zip, test_images.zip in ./data/
  - NOTE: ZIPs are named with _images suffix, not just train.zip/test.zip
  - Files are at root level in ZIPs (no internal subdirectory)
  - Extract to current directory with directory name matching expected path
  - Pattern:
    ```python
    import zipfile

    # Extract train_images.zip
    if os.path.exists("./data/train_images.zip") and not os.path.exists("./train_images"):
        with zipfile.ZipFile("./data/train_images.zip", "r") as z:
            z.extractall("./train_images")

    # Extract test_images.zip
    if os.path.exists("./data/test_images.zip") and not os.path.exists("./test_images"):
        with zipfile.ZipFile("./data/test_images.zip", "r") as z:
            z.extractall("./test_images")

    # Then use ./train_images and ./test_images as paths
    image_dir = "./train_images"
    test_image_dir = "./test_images"
    ```

statoil-iceberg-classifier-challenge:
  - Data files: train.json.7z, test.json.7z, sample_submission.csv.7z in ./data/
  - These are JSON files compressed with 7z format
  - MUST extract to current directory using py7zr (with self-contained install)
  - Pattern:
    ```python
    import subprocess
    from pathlib import Path

    # Install py7zr if not available
    try:
        import py7zr
    except ImportError:
        subprocess.run(['pip', 'install', 'py7zr'], check=True)
        import py7zr

    DATA_PATH = Path("./data")
    TRAIN_FILE = Path("./train.json")
    TEST_FILE = Path("./test.json")

    TRAIN_7Z = DATA_PATH / "train.json.7z"
    TEST_7Z = DATA_PATH / "test.json.7z"

    if TRAIN_7Z.exists() and not TRAIN_FILE.exists():
        with py7zr.SevenZipFile(TRAIN_7Z, mode='r') as z:
            z.extractall(path=".")

    if TEST_7Z.exists() and not TEST_FILE.exists():
        with py7zr.SevenZipFile(TEST_7Z, mode='r') as z:
            z.extractall(path=".")
    ```

freesound-audio-tagging-2019:
  - Data files: train_curated.zip, train_noisy.zip, test.zip in ./data/
  - These are audio files (WAV) with files at root level in ZIPs (no internal subdirectories)
  - CSVs are also in ./data/: train_curated.csv, train_noisy.csv, sample_submission.csv
  - MUST extract ZIPs to current directory, creating subdirectories to organize files
  - Pattern:
    ```python
    import zipfile
    from pathlib import Path

    DATA_ROOT = Path("./data")

    # Extract audio files from ZIP archives to current directory
    if (DATA_ROOT / "train_curated.zip").exists() and not Path("train_curated").exists():
        with zipfile.ZipFile(DATA_ROOT / "train_curated.zip", "r") as z:
            z.extractall("train_curated")

    if (DATA_ROOT / "train_noisy.zip").exists() and not Path("train_noisy").exists():
        with zipfile.ZipFile(DATA_ROOT / "train_noisy.zip", "r") as z:
            z.extractall("train_noisy")

    if (DATA_ROOT / "test.zip").exists() and not Path("test").exists():
        with zipfile.ZipFile(DATA_ROOT / "test.zip", "r") as z:
            z.extractall("test")

    # Update code to look in extracted directories
    # BEFORE: base = DATA_ROOT / "train_curated"
    # AFTER:  base = Path("train_curated")
    ```
  - CRITICAL: Code must be updated to look in ./train_curated, ./train_noisy, ./test instead of ./data/train_curated, etc.
  - Extract AFTER loading CSVs from ./data/ but BEFORE creating datasets that need the audio files

herbarium-2022-fgvc9:
  - Data files: train_images/, test_images/ directories already extracted in ./data/
  - NO ZIP FILES to extract - data is already uncompressed
  - Directory structure: ./data/train_images/ABC/DE/ABCDE__###.jpg where ABC is first 3 chars of image_id, DE is chars 3-4
  - Metadata format: image_id is a STRING like "00000__001", not an integer
  - Common errors in buggy code:
    1. Wrong base directory: uses "h22-train/images" instead of "train_images"
    2. Incorrect folder extraction: uses sid[-2:] (last 2 chars) instead of sid[3:5] (chars at positions 3-4)
    3. Unnecessary zero-padding: uses str(image_id).zfill(8) when image_id is already properly formatted
  - Pattern for CORRECT path construction:
    ```python
    def _image_path(self, image_id):
        if self.is_train:
            sid = str(image_id)  # No zfill needed
            folder1 = sid[:3]    # First 3 characters
            folder2 = sid[3:5]   # Characters at positions 3-4 (NOT sid[-2:])
            return (
                DATA_ROOT
                / "train_images"  # NOT "h22-train/images"
                / folder1
                / folder2
                / f"{image_id}.jpg"
            )
    ```
  - Example: image_id "11741__001" -> train_images/117/41/11741__001.jpg
  - Test images: ./data/test_images/000/test-000000.jpg (standard structure, usually no bug)

kuzushiji-recognition:
  - Data files: train_images.zip, test_images.zip in ./data/
  - These contain JPG image files at root level (no internal subdirectory)
  - Code expects ./data/train_images/ and ./data/test_images/ directories but only ZIPs exist
  - MUST extract to current directory, creating subdirectories to match expected paths
  - Pattern:
    ```python
    import zipfile

    data_dir = "./data"
    train_zip = os.path.join(data_dir, "train_images.zip")
    test_zip = os.path.join(data_dir, "test_images.zip")

    # Extract to current directory with appropriate subdirectory names
    if os.path.exists(train_zip) and not os.path.exists("./train_images"):
        with zipfile.ZipFile(train_zip, "r") as z:
            z.extractall("./train_images")

    if os.path.exists(test_zip) and not os.path.exists("./test_images"):
        with zipfile.ZipFile(test_zip, "r") as z:
            z.extractall("./test_images")

    # Update paths to use extracted directories
    train_img_dir = "./train_images"
    test_img_dir = "./test_images"
    ```
  - CRITICAL: Extract creates subdirectory for files at root level, so ./train_images/image.jpg
  - Original buggy code had paths like os.path.join(data_dir, "train_images") expecting a directory that doesn't exist

hubmap-kidney-segmentation:
  - Data files: train/, test/ directories already extracted in ./data/
  - NO ZIP FILES to extract - data is already uncompressed
  - Contains TIFF files: ./data/train/*.tiff, ./data/test/*.tiff
  - CRITICAL: These are specialized medical imaging TIFF files that PIL cannot read
  - Common error: UnidentifiedImageError: cannot identify image file 'data/train/c68fe75ea.tiff'
  - Root cause: PIL's Image.open() cannot decode multi-page or specialized TIFF formats
  - Solution: Use tifffile library instead of PIL for loading images
  - Pattern:
    ```python
    import tifffile
    from PIL import Image

    def _load_image(self, path):
        """Load image with tifffile, return HWC uint8 array."""
        img = tifffile.imread(str(path), squeeze=True)  # CRITICAL: squeeze=True removes singleton dims
        # Handle different TIFF formats
        if img.ndim == 2:
            # Grayscale - convert to RGB by stacking
            img = np.stack([img, img, img], axis=-1)
        elif img.shape[0] == 3:
            # Channel-first format - transpose to HWC
            img = img.transpose(1, 2, 0)
        return img
    ```
  - IMPORTANT: Apply tifffile loading in both dataset __getitem__ and inference predict_probs
  - After loading with tifffile, can still use PIL for resizing: Image.fromarray(img).resize()
  - No data extraction needed - images already exist in ./data/train/ and ./data/test/

3d-object-detection-for-autonomous-vehicles:
  - Data files: train_lidar/, train_images/, test_lidar/, test_images/ directories already extracted in ./data/
  - Also contains metadata JSON files in ./data/train_data/ and ./data/test_data/
  - NO ZIP FILES to extract - data is already uncompressed
  - Uses nuScenes dataset format with complex multi-step metadata lookup
  - CRITICAL: Cannot directly map CSV Id tokens to filenames - requires JSON metadata chain
  - Common error: Trying to use sample tokens directly as filenames like "token.bin"
  - Root cause: nuScenes format requires 4-step lookup chain to map sample tokens to actual file paths
  - Metadata structure:
    * sensor.json: Maps sensor_token to channel name (LIDAR_TOP, CAM_FRONT, etc.)
    * calibrated_sensor.json: Maps calibrated_sensor_token to sensor_token
    * sample_data.json: Maps sample_token to calibrated_sensor_token and filename
    * sample.json: Contains sample tokens (used as CSV Id column)
  - Pattern for CORRECT file lookup:
    ```python
    import json

    # Build lookup chain
    with open("./data/train_data/sensor.json", "r") as f:
        sensor_list = json.load(f)
    sensor_by_token = {item["token"]: item["channel"] for item in sensor_list}

    with open("./data/train_data/calibrated_sensor.json", "r") as f:
        calibrated_sensor_list = json.load(f)
    calibrated_to_sensor = {item["token"]: item["sensor_token"] for item in calibrated_sensor_list}

    sensor_channels = {calib_token: sensor_by_token.get(sensor_token, "")
                       for calib_token, sensor_token in calibrated_to_sensor.items()}

    with open("./data/train_data/sample_data.json", "r") as f:
        sample_data_list = json.load(f)

    # Group sample_data by sample_token
    sample_data_by_sample = {}
    for sd in sample_data_list:
        sample_token = sd.get("sample_token", "")
        if sample_token not in sample_data_by_sample:
            sample_data_by_sample[sample_token] = []
        sample_data_by_sample[sample_token].append(sd)

    # In __getitem__, lookup files for a sample
    sample_token = annotations.iloc[idx]["Id"]
    sample_data_list = sample_data_by_sample.get(sample_token, [])

    lidar_filename = ""
    image_filename = ""
    for sd in sample_data_list:
        channel = sensor_channels.get(sd.get("calibrated_sensor_token", ""), "")
        if channel == "LIDAR_TOP":
            lidar_filename = sd.get("filename", "")
        elif channel == "CAM_FRONT":
            image_filename = sd.get("filename", "")

    # Strip directory prefixes since base paths already include them
    if lidar_filename.startswith("lidar/"):
        lidar_filename = lidar_filename[6:]
    if image_filename.startswith("images/"):
        image_filename = image_filename[7:]

    lidar_file = os.path.join("./data/train_lidar", lidar_filename)
    image_file = os.path.join("./data/train_images", image_filename)
    ```
  - IMPORTANT: Filenames in sample_data.json include directory prefixes like "lidar/" and "images/"
  - Since base paths already point to train_lidar and train_images, these prefixes must be stripped
  - LIDAR format: .bin files contain 5 float32 values per point (x, y, z, intensity, ring_index)
  - Load LIDAR with: np.fromfile(path, dtype=np.float32).reshape(-1, 5)
  - Point clouds have variable numbers of points - cannot use default PyTorch batching
  - Repeat the entire lookup chain for test_data using ./data/test_data/ JSON files

See finished_files/ for working examples of both cases.

================================================================================
