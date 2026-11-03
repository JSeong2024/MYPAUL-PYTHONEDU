# **Problem 5.3.4. 2차원 리스트 원소의 합**
## 배경 지식(Background)
### 2차원 리스트
```
arr2d = [0, [1, 2], [3], 4, 5]

print(f"arr2d[0]: {arr2d[0]}")
print(f"arr2d[1]: {arr2d[1]}")
print(f"arr2d[2]: {arr2d[2]}")
print(f"arr2d[3]: {arr2d[3]}")
print(f"arr2d[4]: {arr2d[4]}")
```
```
arr2d[0]: 0
arr2d[1]: [1, 2]
arr2d[2]: [3]
arr2d[3]: 4
arr2d[4]: 5
```

<br/>

```
arr2d = [0, [1, 2], [3], 4, 5]

print(f"arr2d[1][0]: {arr2d[1][0]}")
print(f"arr2d[1][1]: {arr2d[1][1]}")
print(f"arr2d[2][0]: {arr2d[2][0]}")
```
```
arr2d[1][0]: 1
arr2d[1][1]: 2
arr2d[2][0]: 3
```
<br/>

### 리스트 연산
```
# 리스트 덧셈
[1, 2] + [3, 4]
```
`[1, 2, 3, 4]`

<br/>

```
# 리스트 곱셈
[1, 2] * 3
```
`[1, 2, 1, 2, 1, 2]`

<br/>

### sum()
```
a = [10, 20, 30, 40, 50]
sum(a)
```
`150`

---
## Question

- `matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]`
- matrix 리스트의 모든 원소의 합을 구해보자.
