"""Mini 01: 문의 우선 처리 분류와 오분류 분석."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ["waiting_hours", "failed_attempts", "impacted_users"]


def load_data(path=ROOT / "data/service_tickets.csv"):
    df = pd.read_csv(path)
    required = ["ticket_id", *FEATURES, "urgent"]
    if any(c not in df.columns for c in required):
        raise ValueError("필수 열이 없습니다.")
    if df[required].isna().any().any() or df.ticket_id.duplicated().any():
        raise ValueError("결측값 또는 중복 ticket_id가 있습니다.")
    for col in FEATURES:
        if not pd.api.types.is_numeric_dtype(df[col]) or not np.isfinite(df[col].to_numpy()).all():
            raise ValueError("Feature는 유한한 숫자여야 합니다.")
        if (df[col] < 0).any():
            raise ValueError("Feature에는 음수 값을 사용할 수 없습니다.")
    if not df.urgent.isin([0, 1]).all():
        raise ValueError("urgent는 0 또는 1이어야 합니다.")
    if df.urgent.nunique() < 2:
        raise ValueError("두 클래스가 모두 필요합니다.")
    return df


def train_model(df):
    X = df[FEATURES].to_numpy(dtype=float)
    y = df["urgent"].to_numpy(dtype=int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y)
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42))
    model.fit(X_train, y_train)
    predicted = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]
    return {
        "model": model, "X_test": X_test, "y_test": y_test,
        "predicted": predicted, "probabilities": probabilities,
        "accuracy": float(accuracy_score(y_test, predicted)),
        "confusion": confusion_matrix(y_test, predicted, labels=[0, 1]),
    }


def plot_result(result, output=ROOT / "outputs/mini_01_ticket_classification.png"):
    output = Path(output)
    output.parent.mkdir(exist_ok=True, parents=True)
    matrix = result["confusion"]
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    ax.imshow(matrix, cmap="Blues")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(matrix[i, j]), ha="center", va="center", color="black")
    ax.set(xticks=[0, 1], yticks=[0, 1], xticklabels=["Normal", "Urgent"],
           yticklabels=["Normal", "Urgent"], xlabel="Predicted", ylabel="Actual",
           title="Ticket classification: confusion matrix")
    fig.tight_layout()
    fig.savefig(output, dpi=140)
    plt.close(fig)
    return output


def main():
    result = train_model(load_data())
    print(f"Accuracy: {result['accuracy']:.1%}")
    print("Confusion matrix:\n", result["confusion"])
    print("Saved:", plot_result(result))

if __name__ == "__main__":
    main()
