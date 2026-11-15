
import os

import joblib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

os.makedirs("ml_results", exist_ok=True)

# Load the trained model
saved = joblib.load("ml_results/random_forest_model.joblib")
model = saved["model"]
features = saved["features"]

# Confusion matrix from the completed test run
# Rows = actual labels; columns = predicted labels
cm = np.array([
    [38663, 90],
    [191, 9056]
])

fig, ax = plt.subplots(figsize=(6, 5))

ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["BENIGN", "ATTACK"]
).plot(ax=ax, cmap="Blues", values_format="d")

ax.set_title("Random Forest - Confusion Matrix")
fig.tight_layout()
fig.savefig("ml_results/confusion_matrix.png", dpi=200)
plt.close(fig)

# Feature importance from the saved Random Forest model
forest = model.named_steps["classifier"]
importance = forest.feature_importances_

order = np.argsort(importance)

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(
    np.array(features)[order],
    importance[order]
)

ax.set_xlabel("Feature Importance")
ax.set_title("Random Forest - Feature Importance")
fig.tight_layout()
fig.savefig("ml_results/feature_importance.png", dpi=200)
plt.close(fig)

print("Visualization files created:")
print("ml_results/confusion_matrix.png")
print("ml_results/feature_importance.png")
