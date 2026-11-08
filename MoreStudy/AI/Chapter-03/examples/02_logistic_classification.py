"""Logistic Regression으로 Ticket의 긴급 Label을 분류한다."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "solutions"))
from mini_01_ticket_classification import load_data, train_model

result = train_model(load_data())
print(f"Accuracy: {result['accuracy']:.1%}")
print("Confusion matrix (rows=actual, cols=predicted):")
print(result["confusion"])
print("First 5 probabilities:", result["probabilities"][:5].round(3).tolist())
