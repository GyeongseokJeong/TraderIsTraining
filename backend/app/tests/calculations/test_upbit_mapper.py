from app.features.candles.enums import Timeframe
from app.integrations.upbit.mapper import normalize_upbit_candles


def test_normalize_upbit_candles_sorts_ascending() -> None:
    payloads = [
        {"market": "KRW-BTC", "candle_date_time_utc": "2024-01-02T00:00:00", "candle_date_time_kst": "2024-01-02T09:00:00", "opening_price": 2, "high_price": 3, "low_price": 1, "trade_price": 2, "candle_acc_trade_volume": 1, "candle_acc_trade_price": 2},
        {"market": "KRW-BTC", "candle_date_time_utc": "2024-01-01T00:00:00", "candle_date_time_kst": "2024-01-01T09:00:00", "opening_price": 1, "high_price": 2, "low_price": 1, "trade_price": 1, "candle_acc_trade_volume": 1, "candle_acc_trade_price": 1},
    ]
    candles = normalize_upbit_candles(payloads, Timeframe.day)
    assert candles[0]["candle_time_utc"].isoformat().startswith("2024-01-01")
