import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.enums import enum_values
from app.features.trades.enums import TradeSide


class Trade(Base):
    __tablename__ = "trades"
    __table_args__ = (Index("ix_trades_session_time", "session_id", "candle_time_utc"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("training_sessions.id", ondelete="CASCADE"), index=True)
    side: Mapped[TradeSide] = mapped_column(Enum(TradeSide, name="trade_side", values_callable=enum_values))
    candle_time_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    price: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    quantity: Mapped[Decimal] = mapped_column(Numeric(38, 18))
    gross_amount: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    fee: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    net_amount: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    realized_pnl: Mapped[Decimal | None] = mapped_column(Numeric(28, 10), nullable=True)
    cash_after: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    position_qty_after: Mapped[Decimal] = mapped_column(Numeric(38, 18))
    avg_entry_price_after: Mapped[Decimal] = mapped_column(Numeric(28, 10))
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
