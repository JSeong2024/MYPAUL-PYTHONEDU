"""Shared, tested input and HTML-export utilities for Chapter 07."""
from pathlib import Path
import json
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def export_html(fig: go.Figure, target: Path) -> Path:
    """Save offline HTML with a local Plotly.js copy (no CDN dependency)."""
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        str(target), full_html=True, include_plotlyjs="directory",
        config={"displaylogo": False, "responsive": True},
    )
    return target


def export_json(obj, target: Path) -> Path:
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    return target
