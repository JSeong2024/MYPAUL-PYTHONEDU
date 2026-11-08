"""서로 단위가 다른 Feature를 StandardScaler로 처리합니다."""
from pathlib import Path
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

DATA = Path(__file__).resolve().parents[1] / "data" / "sensor_signals.csv"
frame = pd.read_csv(DATA)
X = frame[["vibration_mm_s", "ambient_lux"]]
y = frame["fault_label"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
raw = KNeighborsClassifier(n_neighbors=7).fit(X_train, y_train)
scaled = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=7))
scaled.fit(X_train, y_train)
print(f"Without scaling: {accuracy_score(y_test, raw.predict(X_test)):.1%}")
print(f"With scaling: {accuracy_score(y_test, scaled.predict(X_test)):.1%}")
