# **Problem 4.1. 피라미드 만들기**

## 배경 지식
- 문자열의 연산을 활용하면 복잡한 그림을 쉽게 만들 수 있다.
- 예를 들어, 다음의 코드를 실행하면 어떻게 될까?
  ```
  print('★')
  print('★'*2)
  print('★'*3)
  ```
  <img width="340" height="283" alt="image" src="https://github.com/user-attachments/assets/7a6bec80-94a6-4b28-ac85-ba51056d909d" />

  문자열에 숫자(정수)를 곱하면, 곱한 숫자 만큼 같은 문자가 복사된다는 것을 알 수 있다.
  즉, `'★'*2` 는 '★'라는 문자열에 2를 곱했으므로 '★'가 2번 나온 것이고, `'★'*3` 은 '★'라는 문자열에 3을 곱했으므로 '★'가 3번 나타난 것이다.

- 이번에는 **공백**을 추가해보자.
  ```
  print(' '*2+'★')
  print('★'*2)
  ```  
  <img width="256" height="216" alt="image" src="https://github.com/user-attachments/assets/a034f910-23d4-4a0c-9b7d-1eea30501532" />

  `print(' '*2+'★')`부분을 살펴보면, `' '*2+'★'` 즉, 공백(`' '`)에 2를 곱한것에 '★'를 더했다. 공백(띄어쓰기 1칸)에 2를 곱하면 공백이 2칸 만들어 지는 것이고, 문자열의 덧셈에 의해 그 뒤에 '★'이 붙어져 나온 것이다.

## 문제
- 위의 코드들을 활용해서 아래와 같이 **3층 별 피라미드를 출력하는 코드**를 만들어 보자.

  <img width="339" height="281" alt="image" src="https://github.com/user-attachments/assets/73dcf952-23e4-4d16-a0f6-6b87efa259de" />
