import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.timestamps import TimestampMixin
from app.features.candles.enums import Timeframe
from app.features.training_sessions.enums import TrainingSessionMode, TrainingSessionStatus


class TrainingSession(Base, TimestampMixin):
    __tablename__ = "training_sessions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    market_code: Mapped[str] = mapped_column(String(20), index=True)
    timeframe: Mapped[Timeframe] = mapped_column(Enum(Timeframe, name="timeframe"))
    start_time_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    initial_visible_count: Mapped[int] = mapped_column(Integer)
    current_index: Mapped[int] = mapped_column(Integer)
    total_candle_count: Mapped[int] = mapped_column(Integer)
    initial_capital: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    fee_rate: Mapped[Decimal] = mapped_column(Numeric(18, 10))
    cash: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    position_qty: Mapped[Decimal] = mapped_column(Numeric(38, 18))
    avg_entry_price: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    realized_pnl: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    status: Mapped[TrainingSessionStatus] = mapped_column(Enum(TrainingSessionStatus, name="training_session_status"))
    mode: Mapped[TrainingSessionMode] = mapped_column(Enum(TrainingSessionMode, name="training_session_mode"), default=TrainingSessionMode.personal_review)
    random_seed: Mapped[str | None] = mapped_column(String(100), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
