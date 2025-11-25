import os
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -------------------------------------------------
# 1. Helper utilities
# -------------------------------------------------
def str2list(s):
    """Convert space‑separated string to list of ints."""
    return [int(x) for x in str(s).split()] if pd.notna(s) else []


def list2str(lst):
    """Convert list of ints to space‑separated string."""
    return " ".join(str(x) for x in lst)


def levenshtein(a, b):
    """Standard Levenshtein distance between two int lists."""
    n, m = len(a), len(b)
    if n == 0:
        return m
    if m == 0:
        return n
    prev = list(range(m + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * m
        for j, cb in enumerate(b, 1):
            cost = 0 if ca == cb else 1
            cur[j] = min(
                prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost  # deletion  # insertion
            )  # substitution
        prev = cur
    return prev[m]


# -------------------------------------------------
# 2. Load data
# -------------------------------------------------
DATA_PATH = "./data"
train_path = os.path.join(DATA_PATH, "training.csv")
test_path = os.path.join(DATA_PATH, "test.csv")

train_df = pd.read_csv(train_path)  # columns: Id, Sequence
test_df = pd.read_csv(test_path)  # columns: Id

train_df["SeqList"] = train_df["Sequence"].apply(str2list)

# -------------------------------------------------
# 3. 5‑fold CV with n‑gram TF‑IDF + cosine NN
# -------------------------------------------------
kf = KFold(n_splits=5, shuffle=True, random_state=42)

total_lev = 0
total_len = 0

for fold, (train_idx, val_idx) in enumerate(kf.split(train_df), 1):
    tr = train_df.iloc[train_idx].reset_index(drop=True)
    val = train_df.iloc[val_idx].reset_index(drop=True)

    # ---- 3.1 Build TF‑IDF on training fold (unigram + bigram) ----
    # Convert each sequence to a space‑separated string (tokens are numbers)
    tr_strings = tr["Sequence"].astype(str).tolist()
    vectorizer = TfidfVectorizer(
        analyzer="word", token_pattern=r"\d+", ngram_range=(1, 2), norm="l2"
    )  # L2‑normalisation
    tr_tfidf = vectorizer.fit_transform(tr_strings)  # shape (n_train, vocab)

    # ---- 3.2 For each validation sample find most similar training sequence ----
    val_strings = val["Sequence"].astype(str).tolist()
    # Transform validation sequences using the same vectorizer (note: some n‑grams may be unseen → zero rows)
    val_tfidf = vectorizer.transform(val_strings)

    # Cosine similarity = dot product because rows are L2‑normalised
    sim_matrix = val_tfidf.dot(tr_tfidf.T)  # shape (n_val, n_train)

    # For each validation row pick the training index with max similarity
    best_train_idx = np.argmax(sim_matrix.toarray(), axis=1)

    for i, row in val.iterrows():
        true_seq = row["SeqList"]
        pred_seq = tr.iloc[best_train_idx[i - val.index[0]]]["SeqList"]
        total_lev += levenshtein(true_seq, pred_seq)
        total_len += len(true_seq)

cv_score = total_lev / total_len if total_len > 0 else float("inf")
print(f"5‑fold CV Levenshtein‑based error rate: {cv_score:.6f}")

# -------------------------------------------------
# 4. Train on full data & predict test set
# -------------------------------------------------
full_strings = train_df["Sequence"].astype(str).tolist()
vectorizer_full = TfidfVectorizer(
    analyzer="word", token_pattern=r"\d+", ngram_range=(1, 2), norm="l2"
)
full_tfidf = vectorizer_full.fit_transform(full_strings)  # (n_train, vocab)

# Compute the mean TF‑IDF vector (centroid of the training set)
centroid = full_tfidf.mean(axis=0)  # 1 x vocab sparse matrix
# Cosine similarity between centroid and each training vector (dot product)
centroid_sim = centroid.dot(full_tfidf.T).toarray().ravel()
best_seq_idx = np.argmax(centroid_sim)
best_sequence = train_df.iloc[best_seq_idx]["SeqList"]

# Use this central sequence for every test video
test_predictions = [list2str(best_sequence) for _ in range(len(test_df))]

submission = pd.DataFrame({"Id": test_df["Id"], "Sequence": test_predictions})
submission_path = "submission.csv"
submission.to_csv(submission_path, index=False)

print(f"Submission saved to '{submission_path}'.")
