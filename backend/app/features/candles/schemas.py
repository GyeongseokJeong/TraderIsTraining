from datetime import datetime
from decimal import Decimal

from app.core.schemas import CamelModel
from app.features.candles.enums import Timeframe


class CandleRead(CamelModel):
    market_code: str
    timeframe: Timeframe
    candle_time_utc: datetime
    candle_time_kst: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    trade_price_volume: Decimal | None = None


class CandlesResponse(CamelModel):
    candles: list[CandleRead]
