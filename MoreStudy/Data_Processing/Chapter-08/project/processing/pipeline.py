"""교육용 기상 관측 데이터의 로딩·검증·집계·저장 파이프라인."""

from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

RAW_COLUMNS = [
    "observation_id", "timestamp_local", "station_id", "temperature_c",
    "humidity_pct", "precipitation_mm",
]


@dataclass
class PipelineResult:
    clean: pd.DataFrame
    issues: pd.DataFrame
    audit: pd.DataFrame
    daily: pd.DataFrame
    station: pd.DataFrame
    monthly: pd.DataFrame
    coverage: pd.DataFrame
    report: dict


def load_inputs(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """원본을 모두 문자열로 읽어 검증 이전의 값을 보존합니다."""
    data_dir = Path(data_dir)
    csv_path = data_dir / "weather_observations.csv"
    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        header = next(csv.reader(file), [])
    if len(header) != len(set(header)) or set(header) != set(RAW_COLUMNS):
        raise ValueError("CSV 헤더에 중복, 누락 또는 예상하지 못한 열이 있습니다.")

    raw = pd.read_csv(csv_path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    raw = raw.loc[:, RAW_COLUMNS].copy()
    for col in RAW_COLUMNS:
        raw[col] = raw[col].astype(str).str.strip()
    raw.insert(0, "source_row", np.arange(2, len(raw) + 2))

    with (data_dir / "stations.json").open(encoding="utf-8") as file:
        station_records = json.load(file)
    stations = pd.DataFrame(station_records)
    expected_station_fields = {"station_id", "region", "elevation_m"}
    if not expected_station_fields.issubset(stations.columns):
        raise ValueError("관측소 기준정보에 필요한 필드가 없습니다.")
    stations = stations[["station_id", "region", "elevation_m"]].copy()
    if stations.empty or stations["station_id"].isna().any() or stations["region"].isna().any():
        raise ValueError("관측소 기준정보가 비어 있거나 필수 값이 없습니다.")
    stations["station_id"] = stations["station_id"].astype(str).str.strip()
    stations["region"] = stations["region"].astype(str).str.strip()
    if (stations["station_id"] == "").any() or (stations["region"] == "").any():
        raise ValueError("관측소 ID와 지역명은 비어 있을 수 없습니다.")
    if stations["station_id"].duplicated().any():
        raise ValueError("관측소 기준정보의 station_id는 유일해야 합니다.")
    stations["elevation_m"] = pd.to_numeric(stations["elevation_m"], errors="coerce")
    if stations["elevation_m"].isna().any() or (~np.isfinite(stations["elevation_m"])).any():
        raise ValueError("관측소 고도 값이 유효하지 않습니다.")

    with (data_dir / "cleaning_policy.json").open(encoding="utf-8") as file:
        policy = json.load(file)
    try:
        start, end = date.fromisoformat(policy["date_start"]), date.fromisoformat(policy["date_end"])
        times = policy["expected_times"]
        temp_min, temp_max = float(policy["temperature_c"]["min"]), float(policy["temperature_c"]["max"])
        hum_min, hum_max = float(policy["humidity_pct"]["min"]), float(policy["humidity_pct"]["max"])
        rain_min = float(policy["precipitation_mm"]["min"])
    except (ValueError, KeyError, TypeError) as exc:
        raise ValueError("검증 정책의 필수 설정이 잘못되었습니다.") from exc
    if not (start <= end and isinstance(times, list) and len(times) > 0 and
            len(times) == len(set(times)) and all(isinstance(t, str) and len(t) == 5 and t[2] == ':' and
            t[:2].isdigit() and t[3:].isdigit() and 0 <= int(t[:2]) <= 23 and 0 <= int(t[3:]) <= 59 for t in times) and
            np.isfinite([temp_min, temp_max, hum_min, hum_max, rain_min]).all() and
            temp_min <= temp_max and hum_min <= hum_max):
        raise ValueError("검증 정책의 날짜·시간·수치 범위가 유효하지 않습니다.")
    return raw, stations, policy


def validate_and_clean(raw: pd.DataFrame, stations: pd.DataFrame, policy: dict) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """모든 데이터 행에 사유를 기록하고, 집계할 유효 기록만 분리합니다."""
    work = raw.copy()
    timestamp = pd.to_datetime(work["timestamp_local"], format="%Y-%m-%d %H:%M", errors="coerce")
    numeric = {col: pd.to_numeric(work[col], errors="coerce")
               for col in ("temperature_c", "humidity_pct", "precipitation_mm")}
    reject = pd.Series("", index=work.index, dtype=object)
    review = pd.Series("", index=work.index, dtype=object)

    def mark(target: pd.Series, condition: pd.Series, code: str) -> None:
        target.loc[condition.fillna(False)] += "|" + code

    mark(reject, work["observation_id"].eq(""), "missing_observation_id")
    mark(reject, work["observation_id"].ne("") & work["observation_id"].duplicated(keep="first"),
         "duplicate_observation_id")
    mark(reject, work["station_id"].eq(""), "missing_station_id")
    mark(reject, ~work["station_id"].isin(stations["station_id"]), "unknown_station")
    mark(reject, timestamp.isna(), "invalid_timestamp")
    date_ok = timestamp.dt.date.between(date.fromisoformat(policy["date_start"]),
                                         date.fromisoformat(policy["date_end"]))
    mark(reject, timestamp.notna() & ~date_ok, "date_out_of_scope")
    valid_time = timestamp.dt.strftime("%H:%M").isin(policy["expected_times"])
    mark(reject, timestamp.notna() & ~valid_time, "unexpected_observation_time")
    mark(reject, timestamp.notna() & work["station_id"].ne("") &
         pd.DataFrame({"station_id": work["station_id"], "timestamp": timestamp})
           .duplicated(keep="first"), "duplicate_observation_slot")

    for col in numeric:
        values = numeric[col]
        mark(review, work[col].eq(""), f"missing_{col}")
        mark(review, work[col].ne("") & (values.isna() | ~np.isfinite(values)),
             f"non_numeric_{col}")
    temp = numeric["temperature_c"]
    hum = numeric["humidity_pct"]
    rain = numeric["precipitation_mm"]
    mark(review, temp.notna() & np.isfinite(temp) &
         ~temp.between(policy["temperature_c"]["min"], policy["temperature_c"]["max"]),
         "temperature_out_of_range")
    mark(reject, hum.notna() & np.isfinite(hum) &
         ~hum.between(policy["humidity_pct"]["min"], policy["humidity_pct"]["max"]),
         "humidity_out_of_range")
    mark(reject, rain.notna() & np.isfinite(rain) &
         (rain < policy["precipitation_mm"]["min"]), "negative_precipitation")

    status = pd.Series(np.select([reject.ne(""), review.ne("")],
                                  ["rejected", "review"], default="accepted"), index=work.index)
    reason = (reject + review).str.lstrip("|")
    audit = work.assign(status=status, reason=reason)
    issues = audit.loc[audit["status"].ne("accepted")].copy().reset_index(drop=True)

    accepted_mask = status.eq("accepted")
    clean = work.loc[accepted_mask, ["observation_id", "station_id"]].copy()
    clean["timestamp_local"] = timestamp.loc[accepted_mask].to_numpy()
    for col in numeric:
        clean[col] = numeric[col].loc[accepted_mask].astype(float).to_numpy()
    clean = clean.merge(stations, on="station_id", how="left", validate="many_to_one", indicator=True)
    if not clean["_merge"].eq("both").all():
        raise ValueError("미등록 관측소가 결합 단계에 남았습니다.")
    clean = clean.drop(columns="_merge")
    clean["date"] = clean["timestamp_local"].dt.strftime("%Y-%m-%d")
    clean["year_month"] = clean["timestamp_local"].dt.strftime("%Y-%m")
    clean = clean.sort_values(["station_id", "timestamp_local", "observation_id"]).reset_index(drop=True)
    return clean, issues, audit


def make_summaries(clean: pd.DataFrame, stations: pd.DataFrame, policy: dict) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    daily = (clean.groupby(["station_id", "region", "date"], as_index=False)
             .agg(readings=("observation_id", "size"),
                  avg_temperature_c=("temperature_c", "mean"),
                  avg_humidity_pct=("humidity_pct", "mean"),
                  total_precipitation_mm=("precipitation_mm", "sum"))
             .sort_values(["station_id", "date"]).reset_index(drop=True))
    daily["complete_day"] = daily["readings"].eq(len(policy["expected_times"]))
    station = (clean.groupby(["station_id", "region"], as_index=False)
               .agg(readings=("observation_id", "size"),
                    avg_temperature_c=("temperature_c", "mean"),
                    min_temperature_c=("temperature_c", "min"),
                    max_temperature_c=("temperature_c", "max"),
                    total_precipitation_mm=("precipitation_mm", "sum"))
               .sort_values("station_id").reset_index(drop=True))
    monthly = (clean.groupby(["year_month", "region"], as_index=False)
               .agg(readings=("observation_id", "size"),
                    avg_temperature_c=("temperature_c", "mean"),
                    total_precipitation_mm=("precipitation_mm", "sum"))
               .sort_values(["year_month", "region"]).reset_index(drop=True))
    dates = pd.date_range(policy["date_start"], policy["date_end"], freq="D")
    expected = pd.MultiIndex.from_product(
        [stations["station_id"].sort_values(), dates.strftime("%Y-%m-%d")],
        names=["station_id", "date"],
    ).to_frame(index=False)
    counts = clean.groupby(["station_id", "date"], as_index=False).size().rename(columns={"size": "observed_readings"})
    coverage = expected.merge(counts, on=["station_id", "date"], how="left", validate="one_to_one")
    coverage["observed_readings"] = coverage["observed_readings"].fillna(0).astype(int)
    coverage["expected_readings"] = len(policy["expected_times"])
    coverage["status"] = np.select(
        [coverage["observed_readings"].eq(0), coverage["observed_readings"].lt(coverage["expected_readings"])],
        ["missing", "partial"], default="complete",
    )
    for frame in (daily, station, monthly):
        for col in frame.columns:
            if col.startswith("avg_") or col.startswith("min_") or col.startswith("max_") or col.startswith("total_"):
                frame[col] = frame[col].round(2)
    return daily, station, monthly, coverage


def make_quality_report(audit: pd.DataFrame, clean: pd.DataFrame, coverage: pd.DataFrame) -> dict:
    counts = audit["status"].value_counts().to_dict()
    reasons = Counter(code for value in audit["reason"] if value
                      for code in value.split("|") if code)
    expected = int(coverage["expected_readings"].sum())
    observed = len(clean)
    return {
        "total_raw_rows": int(len(audit)),
        "accepted_rows": int(counts.get("accepted", 0)),
        "review_rows": int(counts.get("review", 0)),
        "rejected_rows": int(counts.get("rejected", 0)),
        "reason_counts": dict(sorted(reasons.items())),
        "expected_observation_slots": expected,
        "valid_observations": observed,
        "missing_observation_slots": expected - observed,
        "coverage_pct": round(observed / expected * 100, 2) if expected else None,
        "missing_station_days": int(coverage["status"].eq("missing").sum()),
        "partial_station_days": int(coverage["status"].eq("partial").sum()),
    }


def run_pipeline(data_dir: Path, output_dir: Path, parquet: bool = False) -> PipelineResult:
    """입력 → 검증 → 집계 → 결과 저장. 원본 파일은 수정하지 않습니다."""
    data_dir, output_dir = Path(data_dir).resolve(), Path(output_dir).resolve()
    if data_dir == output_dir or data_dir in output_dir.parents:
        raise ValueError("출력 폴더는 원본 데이터 폴더와 분리해야 합니다.")
    raw, stations, policy = load_inputs(data_dir)
    clean, issues, audit = validate_and_clean(raw, stations, policy)
    daily, station, monthly, coverage = make_summaries(clean, stations, policy)
    report = make_quality_report(audit, clean, coverage)
    if parquet:
        try:
            import pyarrow  # noqa: F401  선택적 기능의 선행 조건을 먼저 확인
        except ImportError as exc:
            raise RuntimeError("Parquet 저장에는 pyarrow가 필요합니다: pip install pyarrow") from exc
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, df in {
        "cleaned_weather.csv": clean,
        "issues.csv": issues,
        "audit.csv": audit,
        "daily_station_summary.csv": daily,
        "station_summary.csv": station,
        "monthly_region_summary.csv": monthly,
        "coverage.csv": coverage,
    }.items():
        df.to_csv(output_dir / name, index=False, encoding="utf-8-sig", float_format="%.2f")
    with (output_dir / "quality_report.json").open("w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)
        file.write("\n")
    if parquet:
        clean.to_parquet(output_dir / "cleaned_weather.parquet", engine="pyarrow", index=False)
    return PipelineResult(clean, issues, audit, daily, station, monthly, coverage, report)
