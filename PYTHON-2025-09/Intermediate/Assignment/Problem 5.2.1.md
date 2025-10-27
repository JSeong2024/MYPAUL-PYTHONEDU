# **Problem 5.2.1. 리스트 뒤집기**
## 배경 지식(Background)
```
nation = ['한국', '미국', '영국', '일본']
nation.reverse()
print(nation)
```
위의 코드를 실행하면 결과는 다음과 같다.

`['일본', '영국', '미국', '한국']`

---
## Question

- reverse 기능을 함수로 만들고자 한다.
- reverse_list 함수를 정의하고, 다음과 같이 실행되어야 한다.

```
nation = ['한국', '미국', '영국', '일본']
rev_list = reverse_list(nation)
print(rev_list)
```
`['일본', '영국', '미국', '한국']`

---
## Answer
### 1.
```
def reverse_list(arr):
  newlist=[]
  for i in range(len(arr)-1, -1, -1):
    newlist.append(arr[i])
  return newlist

reverse_list(nation)
```
<img width="658" height="405" alt="image" src="https://github.com/user-attachments/assets/4d4efd48-462f-41db-9f57-e0c0468a949c" />

### 2.
`(arr: list)`와 `-> list`는 무엇을 의미하나요? 주석 표시입니다. ([click here](https://supermemi.tistory.com/entry/Python-3-%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%97%90%EC%84%9C-%EC%9D%98%EB%AF%B8%EB%8A%94-%EB%AC%B4%EC%97%87%EC%9D%BC%EA%B9%8C-%EC%A3%BC%EC%84%9D#google_vignette))
```
def reverse_list(arr: list) -> list: 
  newlist=[]
  len_list=len(arr)
  for i in range(len_list):
    newlist.append(arr[len_list-1-i])
  return newlist

reverse_list(nation)
```
<img width="657" height="359" alt="image" src="https://github.com/user-attachments/assets/c75bca26-bb92-4bff-8250-982e3f0c7b01" />

### 3. 음수 indexing
```
def reverse_list(arr):
  newlist=[]
  for i in range(1, len(arr)+1):
    newlist.append(arr[-1*i])
  return newlist

reverse_list(nation)
```
<img width="658" height="359" alt="image" src="https://github.com/user-attachments/assets/1725312f-370c-4524-9e5f-f865c12378ed" />

<img width="662" height="216" alt="image" src="https://github.com/user-attachments/assets/330a302d-76b6-4e9e-a5eb-49de0e5fc6cc" />


### 4. 리스트 Slicing
```
def reverse_list(arr):
  return arr[::-1]

reverse_list(nation)
```
