"""Simple, auditable visualization design for synthetic library visits."""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

EXPECTED_BRANCHES = ("Central", "Riverside", "Hilltop", "Eastgate")
START = "2026-10-01"
END = "2026-10-14"
REQUIRED = ("date", "branch", "visitors", "new_members", "event_day")


def load_visits(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, dtype={"branch": "string"})
    if tuple(frame.columns) != REQUIRED:
        raise ValueError(f"Unexpected columns: {list(frame.columns)}")
    frame["date"] = pd.to_datetime(frame["date"], format="%Y-%m-%d", errors="raise")
    if frame.empty or frame[list(REQUIRED)].isna().any().any():
        raise ValueError("Missing values or empty dataset")
    for name in ("visitors", "new_members", "event_day"):
        if not pd.api.types.is_integer_dtype(frame[name]):
            raise ValueError(f"{name} must contain integers")
    if not frame["branch"].isin(EXPECTED_BRANCHES).all():
        raise ValueError("Unknown branch")
    if frame.duplicated(["date", "branch"]).any():
        raise ValueError("Duplicate branch/date record")
    if not frame["date"].between(pd.Timestamp(START), pd.Timestamp(END)).all():
        raise ValueError("Date outside observation window")
    if (frame["visitors"] < 0).any() or (frame["new_members"] < 0).any():
        raise ValueError("Counts cannot be negative")
    if (frame["new_members"] > frame["visitors"]).any():
        raise ValueError("New member count exceeds visitors")
    if not frame["event_day"].isin([0, 1]).all():
        raise ValueError("event_day must be 0 or 1")
    return frame.sort_values(["date", "branch"]).reset_index(drop=True)


def branch_summary(frame: pd.DataFrame) -> pd.DataFrame:
    group = frame.groupby("branch", observed=True, as_index=False).agg(
        observed_days=("date", "nunique"),
        visitors=("visitors", "sum"),
        new_members=("new_members", "sum"),
    )
    group["mean_daily_visitors"] = group["visitors"] / group["observed_days"]
    group["signup_rate_pct"] = np.where(
        group["visitors"] > 0,
        100 * group["new_members"] / group["visitors"],
        np.nan,
    )
    return group.sort_values("visitors", ascending=False).reset_index(drop=True)


def completeness(frame: pd.DataFrame) -> pd.DataFrame:
    dates = pd.date_range(START, END)
    grid = pd.MultiIndex.from_product([dates, EXPECTED_BRANCHES], names=["date", "branch"])
    result = frame.set_index(["date", "branch"])[["visitors"]].reindex(grid).reset_index()
    result["observed"] = result["visitors"].notna()
    return result


def _save(fig, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


def make_charts(frame: pd.DataFrame, output: Path) -> list[Path]:
    summary = branch_summary(frame)
    generated = []

    # Chart 1: counts are encoded by bar length; zero is meaningful.
    fig, ax = plt.subplots(figsize=(8.1, 4.2))
    bars = ax.barh(summary["branch"], summary["visitors"])
    ax.invert_yaxis()
    ax.set_xlim(0, summary["visitors"].max() * 1.22)
    ax.bar_label(bars, padding=4, fmt="%.0f")
    ax.set(title="Total Visitors by Branch (Observed Days)", xlabel="Visitors (people)")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    out = output / "branch_totals.png"; _save(fig, out); generated.append(out)

    # Chart 2: dot plot for close values, no bar-height ambiguity.
    ordered = summary.sort_values("mean_daily_visitors")
    fig, ax = plt.subplots(figsize=(8.1, 4.2))
    ax.scatter(ordered["mean_daily_visitors"], ordered["branch"], s=95)
    ax.set(title="Mean Visitors per Observed Day", xlabel="Visitors / observed day")
    ax.grid(axis="x", alpha=.25)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    out = output / "daily_mean_dots.png"; _save(fig, out); generated.append(out)

    # Chart 3: ratio has a defined denominator and a zero baseline.
    ranked = summary.sort_values("signup_rate_pct", ascending=False)
    fig, ax = plt.subplots(figsize=(8.1, 4.2))
    bars = ax.barh(ranked["branch"], ranked["signup_rate_pct"])
    ax.invert_yaxis()
    ax.set_xlim(0, max(25.0, float(ranked["signup_rate_pct"].max()) * 1.28))
    ax.bar_label(bars, fmt="%.1f%%", padding=4)
    ax.set(title="New Members / Visitors (Observed Records)", xlabel="Rate (%)")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    out = output / "signup_rates.png"; _save(fig, out); generated.append(out)

    # Chart 4: gaps remain gaps (no invented zero values).
    complete = completeness(frame)
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 6.1), sharex=True, sharey=True)
    for ax, branch in zip(axes.flat, EXPECTED_BRANCHES):
        one = complete.loc[complete["branch"].eq(branch)]
        ax.plot(one["date"], one["visitors"], marker="o", markersize=3)
        ax.set_title(branch)
        ax.grid(alpha=.2)
        ax.tick_params(axis="x", rotation=30)
    fig.suptitle("Daily Visitors (Missing ≠ Zero)")
    fig.supxlabel("October 2026")
    fig.supylabel("Visitors (people / day)")
    fig.tight_layout()
    out = output / "daily_trends.png"; _save(fig, out); generated.append(out)

    # Chart 5: coverage is measured against all expected slots.
    days = complete.groupby("branch", observed=True)["observed"].agg(["sum", "size"])
    fig, ax = plt.subplots(figsize=(8.1, 4.1))
    ax.barh(days.index, days["sum"], label="Observed")
    ax.barh(days.index, days["size"]-days["sum"], left=days["sum"],
            label="Missing", hatch="///", edgecolor="black", color="white")
    ax.set(xlim=(0, 15.5), xlabel="Days", title="Expected Days vs Observed Days")
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    out = output / "data_completeness.png"; _save(fig, out); generated.append(out)
    return generated


def make_report(frame: pd.DataFrame, output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    summary = branch_summary(frame)
    complete = completeness(frame)
    summary.to_csv(output / "branch_summary.csv", index=False, encoding="utf-8-sig")
    complete.loc[~complete["observed"], ["date", "branch"]].to_csv(
        output / "missing_dates.csv", index=False, encoding="utf-8-sig"
    )
    figures = make_charts(frame, output)
    info = {
        "source_rows": int(len(frame)),
        "expected_rows": int(len(complete)),
        "missing_records": int((~complete["observed"]).sum()),
        "total_visitors": int(frame["visitors"].sum()),
        "total_new_members": int(frame["new_members"].sum()),
        "figure_files": [p.name for p in figures],
    }
    import json
    (output / "report.json").write_text(json.dumps(info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return info
