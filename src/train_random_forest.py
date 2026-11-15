
import glob
import os

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

# Features available in CIC-IDS2017
FEATURES = [
    "Destination Port",
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Flow Bytes/s",
    "Flow Packets/s",
]

files = sorted(glob.glob("MachineLearningCVE/*.csv"))

if len(files) != 8:
    raise RuntimeError(
        f"Expected 8 CIC-IDS2017 CSV files, found {len(files)}"
    )

samples = []

for file in files:
    print("Reading:", os.path.basename(file))

    df = pd.read_csv(
        file,
        encoding="latin1",
        usecols=lambda col: col.strip() in FEATURES + ["Label"],
        low_memory=False,
    )

    df.columns = df.columns.str.strip()

    # Reproducible sample from each CSV
    df = df.sample(
        n=min(30000, len(df)),
        random_state=42,
    )

    samples.append(df)

data = pd.concat(samples, ignore_index=True)

# Binary classification:
# 0 = BENIGN, 1 = ATTACK
y = (
    data["Label"].astype(str).str.strip().str.upper()
    != "BENIGN"
).astype(int)

X = data[FEATURES].apply(pd.to_numeric, errors="coerce")
X = X.replace([np.inf, -np.inf], np.nan)

print("\nTotal sampled records:", len(data))
print("Benign records:", int((y == 0).sum()))
print("Attack records:", int((y == 1).sum()))

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

model = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("classifier", RandomForestClassifier(
        n_estimators=50,
        max_depth=15,
        random_state=42,
        n_jobs=-1,
    )),
])

print("\nTraining Random Forest...")
model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("\nMODEL EVALUATION")
print("-----------------------------")
print("Accuracy:", round(accuracy_score(y_test, predictions), 4))

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        target_names=["BENIGN", "ATTACK"],
        zero_division=0,
    )
)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

os.makedirs("ml_results", exist_ok=True)

joblib.dump(
    {"model": model, "features": FEATURES},
    "ml_results/random_forest_model.joblib",
)

print("\nModel saved successfully!")
print("Location: ml_results/random_forest_model.joblib")
