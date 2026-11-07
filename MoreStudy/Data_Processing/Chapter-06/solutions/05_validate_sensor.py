import numpy as np
import pandas as pd


def valid_sensor_rows(frame: pd.DataFrame) -> pd.DataFrame:
    required = {"date", "temperature_c"}
    if not required.issubset(frame.columns):
        raise ValueError("date and temperature_c columns are required")
    text_dates = frame["date"].astype("string")
    date_ok = text_dates.str.fullmatch(r"\d{4}-\d{2}-\d{2}").fillna(False)
    dates = pd.to_datetime(text_dates, format="%Y-%m-%d", errors="coerce")
    values = pd.to_numeric(frame["temperature_c"], errors="coerce")
    valid = date_ok & dates.notna() & values.between(-40, 85) & np.isfinite(values)
    result = pd.DataFrame({"date": dates, "temperature_c": values.astype(float)})
    return result.loc[valid.fillna(False)].reset_index(drop=True)


if __name__ == "__main__":
    demo = pd.DataFrame({
        "date": ["2026-10-01", "2026-02-30", "2026-10-03"],
        "temperature_c": ["23.5", "20", "999"],
    })
    print(valid_sensor_rows(demo))
