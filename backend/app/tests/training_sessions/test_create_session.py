from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.db.session  # noqa: F401
from app.db.base import Base
from app.features.candles.enums import Timeframe
from app.features.candles.models import Candle
from app.features.training_sessions.schemas import TrainingSessionCreate
from app.features.training_sessions.service import TrainingSessionService


class StubCandleService:
    def ensure_candles(self, db, *, market_code, timeframe, start_time_utc, end_time_utc):
        return list(
            db.query(Candle)
            .filter(
                Candle.market_code == market_code,
                Candle.timeframe == timeframe,
                Candle.candle_time_utc >= start_time_utc,
                Candle.candle_time_utc <= end_time_utc,
            )
            .order_by(Candle.candle_time_utc)
            .all()
        )


def _make_candle(index: int, start_time: datetime) -> Candle:
    candle_time = start_time + timedelta(hours=index)
    price = Decimal("100") + Decimal(index)
    return Candle(
        market_code="KRW-BTC",
        timeframe=Timeframe.minute_60,
        candle_time_utc=candle_time,
        candle_time_kst=candle_time,
        open=price,
        high=price + Decimal("1"),
        low=price - Decimal("1"),
        close=price,
        volume=Decimal("1"),
        trade_price_volume=price,
        source="TEST",
    )


def test_create_session_flushes_with_registered_foreign_key_tables() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(engine)

    start_time = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end_time = start_time + timedelta(hours=4)

    with TestingSessionLocal() as db:
        db.add_all(_make_candle(index, start_time) for index in range(5))
        db.commit()

        payload = TrainingSessionCreate(
            market_code="KRW-BTC",
            timeframe=Timeframe.minute_60,
            start_time_utc=start_time,
            end_time_utc=end_time,
            initial_visible_count=2,
        )

        state = TrainingSessionService(candle_service=StubCandleService()).create_session(db, payload)

        assert state.session.market_code == "KRW-BTC"
        assert len(state.visible_candles) == 2
        assert state.account_summary.total_equity == payload.initial_capital
