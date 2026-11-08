"""Binary Classification 평가 지표를 직접 계산한다."""
import numpy as np
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score

actual = np.array([0, 0, 0, 0, 1, 1, 1, 1])
predicted = np.array([0, 0, 1, 0, 0, 1, 1, 0])
tn, fp, fn, tp = confusion_matrix(actual, predicted, labels=[0, 1]).ravel()
precision = tp / (tp + fp) if (tp + fp) else 0.
recall = tp / (tp + fn) if (tp + fn) else 0.
f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.

print(f"TN={tn}, FP={fp}, FN={fn}, TP={tp}")
print(f"Precision={precision:.3f}, Recall={recall:.3f}, F1={f1:.3f}")
print("scikit-learn:",precision_score(actual,predicted),
      recall_score(actual,predicted),f1_score(actual,predicted))
