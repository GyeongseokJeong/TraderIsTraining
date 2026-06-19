import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Enum, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.enums import enum_values
from app.features.candles.enums import Timeframe


class ChallengeTemplate(Base):
    __tablename__ = "challenge_templates"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    market_code: Mapped[str] = mapped_column(String(20))
    timeframe: Mapped[Timeframe] = mapped_column(Enum(Timeframe, name="timeframe", values_callable=enum_values))
    start_time_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    initial_capital: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    fee_rate: Mapped[Decimal] = mapped_column(Numeric(18, 10))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
