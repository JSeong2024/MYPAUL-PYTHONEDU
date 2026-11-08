"""훈련 데이터의 CV에서 Hyperparameter를 고른 뒤 Test 평가."""
from pathlib import Path
import pandas as pd
from sklearn.metrics import f1_score, balanced_accuracy_score
from sklearn.model_selection import GridSearchCV, train_test_split, StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT=Path(__file__).resolve().parents[1]
FEATURES=["temperature_c","vibration_mm_s","current_a","operation_hours"]

def run(df):
    X,y=df[FEATURES].to_numpy(),df.flagged.to_numpy(dtype=int)
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.2,stratify=y,random_state=42)
    pipeline=Pipeline([("scaler",StandardScaler()),("knn",KNeighborsClassifier())])
    grid=GridSearchCV(pipeline,{"knn__n_neighbors":[3,7,15,31],"knn__weights":["uniform","distance"]},
                      cv=StratifiedKFold(5,shuffle=True,random_state=42),scoring="f1",refit=True)
    grid.fit(X_train,y_train)
    test_pred=grid.predict(X_test)
    return {"params":grid.best_params_,"validation_f1":float(grid.best_score_),
            "test_f1":float(f1_score(y_test,test_pred,zero_division=0)),
            "test_balanced_accuracy":float(balanced_accuracy_score(y_test,test_pred))}

if __name__=="__main__":
    print(run(pd.read_csv(ROOT/"data/incident_alerts.csv")))
