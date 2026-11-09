[← Chapter 06](../README.md) · [Contents](../README.md#contents)

# 자동 테스트

```bash
python -m unittest discover -s tests -v
```

- 학생용 `exercises/` 코드는 TODO가 포함된 미완성 코드이므로 자동 테스트는 `solutions/`를 검사합니다.
- 합성 데이터, 출력 Shape, Loss, 모델 저장/복원, Markdown 상대경로를 확인합니다.
- CPU 기준으로 실행하며 GPU나 외부 파일 다운로드를 요구하지 않습니다.
- 학습 결과는 수치적으로 허용 가능한 범위로 점검합니다. 특정 정확도 소수점까지의 일치를 요구하지 않습니다.
