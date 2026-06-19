from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import Field

from app.core.schemas import CamelModel
from app.features.candles.enums import Timeframe
from app.features.candles.schemas import CandleRead
from app.features.trades.enums import TradeSide
from app.features.trades.schemas import TradeRead
from app.features.training_sessions.enums import TrainingSessionMode, TrainingSessionStatus


class TrainingSessionCreate(CamelModel):
    market_code: str = "KRW-BTC"
    timeframe: Timeframe = Timeframe.minute_60
    start_time_utc: datetime
    end_time_utc: datetime
    initial_capital: Decimal = Field(default=Decimal("10000000"), gt=0)
    fee_rate: Decimal = Field(default=Decimal("0.0005"), ge=0, le=Decimal("0.01"))
    initial_visible_count: int = Field(default=80, ge=2)
    random_mode: bool = False


class TradeCreate(CamelModel):
    side: TradeSide
    percentage: int = Field(..., description="25, 50, 75, or 100")
    note: str | None = Field(default=None, max_length=2000)


class TrainingSessionRead(CamelModel):
    id: UUID
    market_code: str
    timeframe: Timeframe
    start_time_utc: datetime
    end_time_utc: datetime
    initial_visible_count: int
    current_index: int
    total_candle_count: int
    initial_capital: Decimal
    fee_rate: Decimal
    cash: Decimal
    position_qty: Decimal
    avg_entry_price: Decimal
    realized_pnl: Decimal
    status: TrainingSessionStatus
    mode: TrainingSessionMode
    finished_at: datetime | None


class AccountSummary(CamelModel):
    initial_capital: Decimal
    cash: Decimal
    position_qty: Decimal
    avg_entry_price: Decimal
    current_price: Decimal
    realized_pnl: Decimal
    unrealized_pnl: Decimal
    total_equity: Decimal
    return_pct: Decimal
    max_drawdown: Decimal


class TrainingSessionState(CamelModel):
    session: TrainingSessionRead
    visible_candles: list[CandleRead]
    trades: list[TradeRead]
    account_summary: AccountSummary
