from datetime import datetime

from sqlalchemy.orm import Session

from app.features.candles.enums import Timeframe
from app.features.candles.models import Candle
from app.features.candles.repository import list_candles, upsert_candles
from app.integrations.upbit.client import UpbitClient
from app.integrations.upbit.mapper import normalize_upbit_candles


class CandleService:
    def __init__(self, upbit_client: UpbitClient | None = None) -> None:
        self.upbit_client = upbit_client or UpbitClient()

    def ensure_candles(self, db: Session, *, market_code: str, timeframe: Timeframe, start_time_utc: datetime, end_time_utc: datetime) -> list[Candle]:
        cached = list_candles(db, market_code=market_code, timeframe=timeframe, start_time_utc=start_time_utc, end_time_utc=end_time_utc)
        if cached:
            return cached
        cursor = end_time_utc
        normalized: list[dict] = []
        for _ in range(30):
            payloads = self.upbit_client.get_candles(market_code=market_code, timeframe=timeframe, to=cursor, count=200)
            if not payloads:
                break
            chunk = normalize_upbit_candles(payloads, timeframe)
            normalized.extend([candle for candle in chunk if start_time_utc <= candle["candle_time_utc"] <= end_time_utc])
            oldest = chunk[0]["candle_time_utc"]
            if oldest <= start_time_utc:
                break
            cursor = oldest
        upsert_candles(db, normalized)
        db.commit()
        return list_candles(db, market_code=market_code, timeframe=timeframe, start_time_utc=start_time_utc, end_time_utc=end_time_utc)
