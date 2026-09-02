"""Download and clean QQQ daily OHLCV data with yfinance."""

from __future__ import annotations

import json
import hashlib
import subprocess
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import yfinance as yf


TICKER = "QQQ"
START_DATE = "2000-01-01"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "data" / "qqq.csv"
SOURCE_PATH = PROJECT_ROOT / "data" / "source.json"
REQUIRED_COLUMNS = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]


def _flatten_yfinance_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize both single-ticker and MultiIndex yfinance responses."""
    if not isinstance(frame.columns, pd.MultiIndex):
        return frame

    ticker_level = frame.columns.get_level_values(-1)
    if TICKER in ticker_level:
        return frame.xs(TICKER, axis=1, level=-1, drop_level=True)

    result = frame.copy()
    result.columns = [str(column[0]) for column in result.columns]
    return result


def fetch_yfinance() -> pd.DataFrame:
    end_date = (date.today() + timedelta(days=1)).isoformat()
    data = yf.download(
        TICKER,
        start=START_DATE,
        end=end_date,
        auto_adjust=False,
        actions=False,
        progress=False,
        threads=False,
    )
    if data.empty:
        raise RuntimeError("yfinance returned no QQQ rows.")

    data = _flatten_yfinance_columns(data).reset_index()
    if "Adj Close" not in data.columns and "Close" in data.columns:
        data["Adj Close"] = data["Close"]

    missing = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing:
        raise RuntimeError(f"Missing required columns: {', '.join(missing)}")

    data = data[REQUIRED_COLUMNS].copy()
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce").dt.tz_localize(None)
    for column in REQUIRED_COLUMNS[1:]:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    data = (
        data.dropna(subset=["Date", "Open", "High", "Low", "Close", "Volume"])
        .drop_duplicates(subset="Date", keep="last")
        .sort_values("Date")
    )
    data = data[(data["Close"] > 0) & (data["Volume"] >= 0)]
    data["Date"] = data["Date"].dt.strftime("%Y-%m-%d")
    data.reset_index(drop=True, inplace=True)
    return data


def fetch_longbridge_fallback() -> pd.DataFrame:
    """Read the same daily fields from Longbridge when Yahoo is rate-limited."""
    rows: list[dict] = []
    today = date.today()
    for year in range(2000, today.year + 1):
        period_start = date(year, 1, 1)
        period_end = min(date(year, 12, 31), today)
        command = [
            "longbridge",
            "kline",
            "history",
            "QQQ.US",
            "--start",
            period_start.isoformat(),
            "--end",
            period_end.isoformat(),
            "--period",
            "day",
            "--adjust",
            "forward",
            "--format",
            "json",
        ]
        completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", check=False)
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or f"Longbridge fallback failed for {year}.")
        rows.extend(json.loads(completed.stdout))
    if not rows:
        raise RuntimeError("Longbridge returned no QQQ rows.")

    data = pd.DataFrame(rows).rename(
        columns={
            "time": "Date",
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
        }
    )
    data["Adj Close"] = data["Close"]
    data = data[REQUIRED_COLUMNS].copy()
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce", utc=True).dt.tz_localize(None)
    for column in REQUIRED_COLUMNS[1:]:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    data = (
        data.dropna(subset=REQUIRED_COLUMNS)
        .drop_duplicates(subset="Date", keep="last")
        .sort_values("Date")
    )
    data = data[(data["Close"] > 0) & (data["Volume"] >= 0)]
    data["Date"] = data["Date"].dt.strftime("%Y-%m-%d")
    data.reset_index(drop=True, inplace=True)
    return data


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        data = fetch_yfinance()
        source = "Yahoo Finance via yfinance"
        adjustment = "Yahoo Finance Adj Close; OHLC unadjusted"
        price_field_note = "Adj Close supplied by Yahoo Finance"
    except RuntimeError as error:
        print(f"Primary source unavailable: {error}")
        print("Trying Longbridge Securities fallback...")
        data = fetch_longbridge_fallback()
        source = "Longbridge Securities (forward-adjusted daily OHLCV fallback)"
        adjustment = "Forward-adjusted OHLC"
        price_field_note = "Adj Close copied from forward-adjusted Close because the source has no separate Adj Close field"
    data.to_csv(OUTPUT_PATH, index=False, float_format="%.6f")
    csv_sha256 = hashlib.sha256(OUTPUT_PATH.read_bytes()).hexdigest()
    metadata = {
        "source": source,
        "price_field": "Adj Close",
        "price_field_note": price_field_note,
        "adjustment": adjustment,
        "start_date": data.iloc[0]["Date"],
        "end_date": data.iloc[-1]["Date"],
        "row_count": len(data),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "csv_sha256": csv_sha256,
    }
    SOURCE_PATH.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print("QQQ data download complete")
    print(f"Source: {source}")
    print(f"Rows: {len(data):,}")
    print(f"Range: {data.iloc[0]['Date']} to {data.iloc[-1]['Date']}")
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
