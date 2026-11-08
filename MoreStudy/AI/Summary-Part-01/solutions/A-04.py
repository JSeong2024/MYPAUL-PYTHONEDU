"""A-04: leak-free scaling and cross-validated KNN parameter search."""
from pathlib import Path
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from common import save_json


def main():
    X,y=make_classification(n_samples=400,n_features=5,n_informative=3,n_redundant=0,random_state=42)
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)
    pipeline=Pipeline([('scaler',StandardScaler()),('model',KNeighborsClassifier())])
    search=GridSearchCV(pipeline,{'model__n_neighbors':[3,5,7]},cv=5,scoring='accuracy',refit=True)
    search.fit(X_train,y_train)
    save_json('best_params.json',{'best_n_neighbors':int(search.best_params_['model__n_neighbors']),'mean_cv_accuracy':round(float(search.best_score_),4)})
    y_pred=search.best_estimator_.predict(X_test)
    save_json('test_metrics.json',{'test_accuracy':round(float(accuracy_score(y_test,y_pred)),4),'test_balanced_accuracy':round(float(balanced_accuracy_score(y_test,y_pred)),4)})
    Path('audit_report.md').write_text(
        '# 평가 절차 감사\n\n'
        '## 원본 코드 문제점\n\n'
        '1. 전체 데이터를 분할하기 전에 StandardScaler.fit_transform을 수행해 Test 분포가 전처리에 누출되었습니다.\n'
        '2. Test 점수를 반복 확인하여 이웃 수를 바꾸면서 Test를 모델 선택에 사용했습니다.\n\n'
        '## 복구한 처리 흐름\n\n'
        '1. 원본 X, y를 먼저 Train/Test로 분할합니다.\n'
        '2. Train 내부의 5-Fold CV에서만 Pipeline의 Scaler를 학습합니다.\n'
        '3. GridSearchCV는 Train에서 모델 후보를 선택하고, Test는 최종 평가에 한 번만 사용합니다.\n'
        '4. 각 Fold의 학습 데이터는 해당 Fold의 스케일러 fitting에만 사용됩니다.\n',encoding='utf-8')


if __name__=='__main__':main()
