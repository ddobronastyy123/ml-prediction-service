from pathlib import Path
import pickle

from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

data = load_breast_cancer()
X, y = data.data, data.target

model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=5000, random_state=42)
)
model.fit(X, y)

model_path = Path("model/model.pkl")
model_path.parent.mkdir(parents=True, exist_ok=True)

with model_path.open("wb") as f:
    pickle.dump(model, f)

print("Model trained and saved to model/model.pkl")
print(f"Samples: {X.shape[0]}")
print(f"Features: {X.shape[1]}")
print(f"Classes: {data.target_names.tolist()}")

