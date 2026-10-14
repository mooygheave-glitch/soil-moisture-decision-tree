from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

df = pd.read_csv("data/processed/soil_moisture_dataset.csv")
df["recorded_at"] = pd.to_datetime(df["recorded_at"], errors="coerce")
df["soil_moisture_adc"] = pd.to_numeric(df["soil_moisture_adc"], errors="coerce")
df["jam_pengukuran"] = df["recorded_at"].dt.hour
df["label"] = df["label"].astype(str).str.strip().str.lower()
df = df.dropna(subset=["soil_moisture_adc", "jam_pengukuran", "label"])
df = df[df["label"].isin(["kering", "basah"])]

X = df[["soil_moisture_adc", "jam_pengukuran"]]
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
model = DecisionTreeClassifier(max_depth=3, class_weight="balanced", random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, pred))
print(classification_report(y_test, pred, zero_division=0))
print("Confusion matrix [kering, basah]:")
print(confusion_matrix(y_test, pred, labels=["kering", "basah"]))
print("\nCAUTION: collection hour is strongly associated with label in current data.")
