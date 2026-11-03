```
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
# 데이터 로드를 위한 URL
url = ''
# pandas를 사용하여 데이터 로드
data = pd.read_csv(url)
# 특성과 타겟으로 데이터 분리
X = data.drop('TargetColumn', axis=1) # 'TargetColumn'을 타겟 열 이름으로
y = data['TargetColumn']
# 훈련 세트와 테스트 세트 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
# 결정 트리 모델 생성 및 훈련
model = DecisionTreeClassifier()
model.fit(X_train, y_train)
# 모델 평가
accuracy = model.score(X_test, y_test)
print("Accuracy:", accuracy)
```
