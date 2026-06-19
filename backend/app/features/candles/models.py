import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, Index, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.enums import enum_values
from app.db.timestamps import TimestampMixin
from app.features.candles.enums import Timeframe


class Candle(Base, TimestampMixin):
    __tablename__ = "candles"
    __table_args__ = (
        UniqueConstraint("market_code", "timeframe", "candle_time_utc", name="uq_candle_identity"),
        Index("ix_candles_market_timeframe_time", "market_code", "timeframe", "candle_time_utc"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    market_code: Mapped[str] = mapped_column(String(20), index=True)
    timeframe: Mapped[Timeframe] = mapped_column(Enum(Timeframe, name="timeframe", values_callable=enum_values), index=True)
    candle_time_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    candle_time_kst: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    open: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    high: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    low: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    close: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    volume: Mapped[Decimal] = mapped_column(Numeric(38, 18))
    trade_price_volume: Mapped[Decimal | None] = mapped_column(Numeric(38, 10), nullable=True)
    source: Mapped[str] = mapped_column(String(20), default="UPBIT")
