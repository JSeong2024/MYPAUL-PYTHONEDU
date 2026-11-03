# **Problem 5.3.3. 중복 요소 제거하기**
## 배경 지식(Background)
```
my_list = ['A', 'p', 'p', 'l', 'e']

while 'p' in my_list:
    my_list.remove('p')

print(my_list)
```
`['A', 'l', 'e']`

<br/>

```
my_list = ['A', 'p', 'p', 'l', 'e']

new_list = [item for item in my_list if item != 'p']

print(new_list)
```
`['A', 'l', 'e']`


---
## Question

- `my_list = [1, 2, 2, 3, 4, 4, 5, 5, 5]`
- **my_list**에서 **중복을 제거**하고 **유일한 값만 포함**된 새 리스트를 만들어 보자. (단, 순서는 유지해야 된다.)

---
## Answer
```
my_list = [1, 2, 2, 3, 4, 4, 5, 5, 5]

new_list = []
for item in my_list:
  if item not in new_list:
    new_list.append(item)

print(new_list)
```
`[1, 2, 3, 4, 5]`
