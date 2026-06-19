from datetime import datetime
from decimal import Decimal
from uuid import UUID

from app.core.schemas import CamelModel
from app.features.trades.enums import TradeSide


class TradeRead(CamelModel):
    id: UUID
    side: TradeSide
    candle_time_utc: datetime
    price: Decimal
    quantity: Decimal
    gross_amount: Decimal
    fee: Decimal
    net_amount: Decimal
    realized_pnl: Decimal | None
    cash_after: Decimal
    position_qty_after: Decimal
    avg_entry_price_after: Decimal
    note: str | None
    created_at: datetime
