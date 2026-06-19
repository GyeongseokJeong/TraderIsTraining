from datetime import datetime
from decimal import Decimal

from app.core.schemas import CamelModel


class EquitySnapshotRead(CamelModel):
    candle_time_utc: datetime
    candle_index: int
    cash: Decimal
    position_qty: Decimal
    current_price: Decimal
    equity: Decimal
    drawdown: Decimal
    created_at: datetime
