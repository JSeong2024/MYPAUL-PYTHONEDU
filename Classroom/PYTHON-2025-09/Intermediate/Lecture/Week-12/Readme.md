`분류분석-이진분류`
```
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, accuracy_score
from sklearn.datasets import load_breast_cancer
import time

#1. 데이터
datasets = load_breast_cancer()
print(datasets.DESCR)
print(datasets.feature_names)

x = datasets.data
y = datasets.target
print(x.shape, y.shape) #(569, 30) (569,)

x_train, x_test, y_train, y_test = train_test_split(
    x, y, train_size=0.7, random_state=100, shuffle=True)

#2. 모델구성
model = Sequential()
model.add(Dense(100, activation='linear', input_dim=30))
model.add(Dense(100, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(1, activation='sigmoid')) # 이진분류는 무조건 아웃풋 활성화
                                          # 활성화 함수를 'sigmoid'로 해줘야한다.

#3. 컴파일, 훈련
model.compile(loss='binary_crossentropy', optimizer='adam', 
              metrics=['accuracy','mse'])

start_time = time.time()
model.fit(x_train, y_train, epochs=100, batch_size=200)
end_time = time.time() - start_time

#4. 평가,예측
loss = model.evaluate(x_test, y_test)
y_predict = model.predict(x_test)

# y_predict = np.where(y_predict > 0.5, 1, 0) # where 반올림
y_predict = np.round(y_predict)
acc = accuracy_score(y_test, y_predict)

print('loss:', loss)
print('accuracy:', acc)
print('걸린시간:', end_time)
```

`Simple Linear Regression - Gradient Descent`
```
import numpy as np


x = np.array(
    [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10],
    [11], [12], [13], [14], [15], [16], [17], [18], [19], [20],
    [21], [22], [23], [24], [25], [26], [27], [28], [29], [30]]
)
y = np.array(
    [[0.94], [1.98], [2.88], [3.92], [3.96], [4.55], [5.64], [6.3], [7.44], [9.1],
    [8.46], [9.5], [10.67], [11.16], [14], [11.83], [14.4], [14.25], [16.2], [16.32],
    [17.46], [19.8], [18], [21.34], [22], [22.5], [24.57], [26.04], [21.6], [28.8]]
)

weight = 0.0
bias = 0.0
learning_rate = 0.005

for epoch in range(10000):
    y_hat = weight * x + bias

    cost = ((y - y_hat) ** 2).mean()

    weight = weight - learning_rate * ((y_hat - y) * x).mean()
    bias = bias - learning_rate * (y_hat - y).mean()

    if (epoch + 1) % 1000 == 0:
        print(f"Epoch : {epoch+1:4d}, Weight : {weight:.3f}, Bias : {bias:.3f}, Cost : {cost:.3f}")
```
