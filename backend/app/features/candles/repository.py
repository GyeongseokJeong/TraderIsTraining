from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.features.candles.enums import Timeframe
from app.features.candles.models import Candle


def list_candles(db: Session, *, market_code: str, timeframe: Timeframe, start_time_utc: datetime, end_time_utc: datetime) -> list[Candle]:
    stmt = (
        select(Candle)
        .where(Candle.market_code == market_code, Candle.timeframe == timeframe, Candle.candle_time_utc >= start_time_utc, Candle.candle_time_utc <= end_time_utc)
        .order_by(Candle.candle_time_utc.asc())
    )
    return list(db.scalars(stmt).all())


def upsert_candles(db: Session, candles: list[dict]) -> None:
    if not candles:
        return
    now = datetime.now(timezone.utc)
    rows = [{**candle, "created_at": now, "updated_at": now} for candle in candles]
    stmt = insert(Candle).values(rows)
    update_columns = {key: getattr(stmt.excluded, key) for key in ["open", "high", "low", "close", "volume", "trade_price_volume", "updated_at"]}
    stmt = stmt.on_conflict_do_update(index_elements=["market_code", "timeframe", "candle_time_utc"], set_=update_columns)
    db.execute(stmt)
