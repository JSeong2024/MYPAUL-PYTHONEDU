# 실습 데이터

모든 CSV는 Chapter 05~07의 문제 조건에 맞게 제작한 **실습용 합성 데이터**입니다. 재생성 방법은 `python tests/generate_data.py`이며, Seed는 42입니다. 재생성 시 기존 CSV와 C-02 예제 Weight가 덮어써집니다.

| 문제 | 입력 파일 |
|---|---|
| A-01 | `sensor_readings.csv`, `calibration.csv` |
| A-02 | `usage.csv` |
| A-03 | `energy.csv` |
| A-04 | `training.csv`, `incoming.csv` |
| P-01 | `maintenance_history.csv`, `incoming_maintenance.csv` |
| P-02 | `microgrid_daily.csv` |
| P-03 | `quality_train.csv` |
| C-01 | `train.csv`, `validation.csv` |
| C-02 | `model_weights.pt`, `model_config.json`, `preprocessing.json`, `reference_cases.csv`, `C-02/incoming.csv` |
| R-01 | `sites.csv`, `history.csv`, `R-01/incoming.csv`, `deployment_manifest.json` |

C-02와 R-01은 A-04의 입력 파일과 이름이 겹치지 않도록 전용 하위 폴더에 `incoming.csv`를 저장했습니다. 각 Solution에서는 이 경로를 사용합니다.

모든 출력 파일은 `outputs/문제번호/`에 생성되며 ZIP에는 포함하지 않습니다. 테스트 결과와 그래프는 제공된 합성 데이터에 해당하며, 일반적인 실제 데이터에서 동일한 성능을 보장하지 않습니다.
