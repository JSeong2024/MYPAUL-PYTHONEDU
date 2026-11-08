# Service Performance — 참고 문서

<a id="p95-linear"></a>
## P95 선형 보간

P95는 누적 비율 95%에 해당하는 응답시간입니다. 유효 요청을 오름차순으로 정렬한 뒤 `pandas.Series.quantile(0.95, interpolation="linear")`를 사용합니다.

예를 들어 `100, 200, 300`ms의 세 값은 순서 인덱스가 `0, 1, 2`입니다. `0.95 × (3 - 1) = 1.9`이므로 두 번째 값(200ms)과 세 번째 값(300ms) 사이를 90% 보간합니다.

$$
P_{95}=200+0.9(300-200)=290\ \mathrm{ms}
$$

이 계산에서 쓰는 선형 보간은 **누락된 관측 시간의 응답시간을 추정해 채우는 방식과 다릅니다**.

<a id="audit"></a>
## 감사 기록

`audit.csv`는 제외된 원본 행마다 `source_row`, `request_id`, `reason_codes`를 기록합니다. 첫 데이터 행의 `source_row`는 헤더 다음 행인 `2`입니다. 여러 문제가 있으면 사유를 세미콜론으로 연결합니다. 중복된 요청 ID는 `duplicated(keep=False)`로 모두 제외합니다.

<a id="error-rate"></a>
## 오류율 분모

$$
\mathrm{Server\ Error\ Rate}(\%)=\frac{N_{\mathrm{5xx}}}{N_{\mathrm{valid}}}\times100
$$

`N_valid=0`이면 해당 비율과 P95는 `자료 없음`입니다. 요청이 10건이고 5xx가 0건이면 서버 오류율은 `0%`입니다.

---
[← Project README](./README.md) · [← Chapter 09](../../README.md)
