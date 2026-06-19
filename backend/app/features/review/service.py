from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.features.candles.repository import list_candles
from app.features.review.calculations import (
    calculate_average_win_loss,
    calculate_buy_and_hold_return,
    calculate_profit_factor,
    calculate_win_rate,
)
from app.features.review.schemas import PerformanceSummary, ReviewResponse
from app.features.training_sessions.calculations import calculate_equity, calculate_return_pct
from app.features.training_sessions.enums import TrainingSessionStatus
from app.features.training_sessions.repository import (
    get_session,
    list_equity_snapshots,
    list_trades,
)


class ReviewService:
    def get_review(self, db: Session, session_id: UUID) -> ReviewResponse:
        session = get_session(db, session_id)
        if session is None:
            raise HTTPException(status_code=404, detail="session not found")
        if session.status != TrainingSessionStatus.finished:
            raise HTTPException(status_code=403, detail="review is available only after session is finished")
        candles = list_candles(db, market_code=session.market_code, timeframe=session.timeframe, start_time_utc=session.start_time_utc, end_time_utc=session.end_time_utc)
        trades = list_trades(db, session.id)
        equity_curve = list_equity_snapshots(db, session.id)
        current_price = candles[session.current_index].close
        final_equity = calculate_equity(cash=session.cash, position_qty=session.position_qty, current_price=current_price)
        unrealized_pnl = (current_price - session.avg_entry_price) * session.position_qty if session.position_qty > 0 else Decimal(0)
        realized_pnls = [trade.realized_pnl for trade in trades if trade.realized_pnl is not None]
        average_win, average_loss = calculate_average_win_loss(realized_pnls)
        first_tradable = candles[session.initial_visible_count - 1].close
        final_close = candles[-1].close
        buy_and_hold_return = calculate_buy_and_hold_return(first_close=first_tradable, final_close=final_close)
        final_return_pct = calculate_return_pct(equity=final_equity, initial_capital=session.initial_capital)
        performance = PerformanceSummary(
            final_equity=final_equity,
            final_return_pct=final_return_pct,
            realized_pnl=session.realized_pnl,
            unrealized_pnl=unrealized_pnl,
            max_drawdown=max([snapshot.drawdown for snapshot in equity_curve], default=Decimal(0)),
            trade_count=len(trades),
            win_rate=calculate_win_rate(realized_pnls),
            average_winning_trade=average_win,
            average_losing_trade=average_loss,
            profit_factor=calculate_profit_factor(realized_pnls),
            buy_and_hold_return=buy_and_hold_return,
            excess_return_vs_buy_and_hold=final_return_pct - buy_and_hold_return,
        )
        return ReviewResponse(session=session, candles=candles, trades=trades, equity_curve=equity_curve, performance=performance)
