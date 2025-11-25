# Circular Debug Pattern Analysis

## Problem: Stuck in Loop for `iwildcam-2020-fgvc7_86b26f9301124e8289d9ace20dba6162`

### Error Progression

| Step | Error | Location | Status |
|------|-------|----------|--------|
| **0** | `ValueError: The least populated class in y has only 1 member` | Line 59 (downsampling split) | ❌ Initial bug |
| **1** | `OSError: broken data stream when reading image file` | Line 181 (image loading) | ✅ Fixed line 59, but new error |
| **2** | `ValueError: The least populated class in y has only 1 member` | Line 94 (train/val split) | ❌ Fixed image issue, but lost train/val fix |
| **3** | `ValueError: The least populated class in y has only 1 member` | Line 94 (train/val split) | ❌ Same error repeating |
| **4** | `ValueError: The least populated class in y has only 1 member` | Line 94 (train/val split) | ❌ Same error repeating |

### Root Cause

**Step 1** had the correct fix for BOTH stratified splits:
- Fixed downsampling split (line 59) ✅
- Fixed train/val split (line 94) ✅ - Added `min_count < 2` check

**Step 2** lost the train/val split fix:
- Kept image verification fix ✅
- But reverted train/val split back to unconditional `stratify=train_labels` ❌

**Steps 3-4** are just repeating step 2's mistake.

### Solution

**Step 5** needs to restore the train/val split fix from **Step 1**:

```python
# Around line 89-96, replace:
train_idx, val_idx = train_test_split(
    indices,
    test_size=0.2,
    stratify=train_labels,  # ❌ This fails if classes have <2 samples
    random_state=42,
)

# With (from step 1):
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
        random_state=42,  # ✅ No stratify
    )
else:
    train_idx, val_idx = train_test_split(
        np.arange(len(train_files)),
        test_size=0.2,
        random_state=42,
        stratify=train_labels,  # ✅ Safe to use stratify
    )
```

### Key Insight

When fixing multiple bugs, make sure to **preserve previous fixes** when creating the next step file. The train/val split fix was correct in step 1 but got lost in step 2.

