import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EquitySnapshot(Base):
    __tablename__ = "equity_snapshots"
    __table_args__ = (
        UniqueConstraint("session_id", "candle_index", name="uq_equity_snapshot_session_index"),
        Index("ix_equity_snapshots_session_index", "session_id", "candle_index"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("training_sessions.id", ondelete="CASCADE"), index=True)
    candle_time_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    candle_index: Mapped[int] = mapped_column(Integer)
    cash: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    position_qty: Mapped[Decimal] = mapped_column(Numeric(38, 18))
    current_price: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    equity: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    drawdown: Mapped[Decimal] = mapped_column(Numeric(18, 10))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
