from decimal import Decimal

from app.core.schemas import CamelModel
from app.features.candles.schemas import CandleRead
from app.features.equity_snapshots.schemas import EquitySnapshotRead
from app.features.trades.schemas import TradeRead
from app.features.training_sessions.schemas import TrainingSessionRead


class PerformanceSummary(CamelModel):
    final_equity: Decimal
    final_return_pct: Decimal
    realized_pnl: Decimal
    unrealized_pnl: Decimal
    max_drawdown: Decimal
    trade_count: int
    win_rate: Decimal | None
    average_winning_trade: Decimal | None
    average_losing_trade: Decimal | None
    profit_factor: Decimal | None
    buy_and_hold_return: Decimal
    excess_return_vs_buy_and_hold: Decimal


class ReviewResponse(CamelModel):
    session: TrainingSessionRead
    candles: list[CandleRead]
    trades: list[TradeRead]
    equity_curve: list[EquitySnapshotRead]
    performance: PerformanceSummary
