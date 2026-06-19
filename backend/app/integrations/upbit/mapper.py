from datetime import datetime, timezone
from decimal import Decimal

from app.features.candles.enums import Timeframe


def _parse_upbit_time(value: str) -> datetime:
    return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)


def normalize_upbit_candle(payload: dict, timeframe: Timeframe) -> dict:
    return {
        "market_code": payload["market"],
        "timeframe": timeframe,
        "candle_time_utc": _parse_upbit_time(payload["candle_date_time_utc"]),
        "candle_time_kst": datetime.fromisoformat(payload["candle_date_time_kst"]).replace(tzinfo=timezone.utc),
        "open": Decimal(str(payload["opening_price"])),
        "high": Decimal(str(payload["high_price"])),
        "low": Decimal(str(payload["low_price"])),
        "close": Decimal(str(payload["trade_price"])),
        "volume": Decimal(str(payload["candle_acc_trade_volume"])),
        "trade_price_volume": Decimal(str(payload.get("candle_acc_trade_price", "0"))),
        "source": "UPBIT",
    }


def normalize_upbit_candles(payloads: list[dict], timeframe: Timeframe) -> list[dict]:
    candles = [normalize_upbit_candle(payload, timeframe) for payload in payloads]
    return sorted(candles, key=lambda candle: candle["candle_time_utc"])
