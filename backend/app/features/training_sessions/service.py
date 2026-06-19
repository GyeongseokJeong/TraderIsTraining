from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.candles.repository import list_candles
from app.features.candles.service import CandleService
from app.features.equity_snapshots.models import EquitySnapshot
from app.features.markets.repository import ensure_market_allowed
from app.features.trades.enums import TradeSide
from app.features.trades.models import Trade
from app.features.training_sessions.calculations import (
    calculate_buy_order,
    calculate_drawdown,
    calculate_equity,
    calculate_return_pct,
    calculate_sell_order,
)
from app.features.training_sessions.enums import TrainingSessionMode, TrainingSessionStatus
from app.features.training_sessions.models import TrainingSession
from app.features.training_sessions.repository import (
    get_session,
    list_equity_snapshots,
    list_trades,
)
from app.features.training_sessions.schemas import (
    AccountSummary,
    TradeCreate,
    TrainingSessionCreate,
    TrainingSessionState,
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


class TrainingSessionService:
    def __init__(self, candle_service: CandleService | None = None) -> None:
        self.candle_service = candle_service or CandleService()

    def create_session(self, db: Session, payload: TrainingSessionCreate) -> TrainingSessionState:
        ensure_market_allowed(payload.market_code)
        if payload.end_time_utc <= payload.start_time_utc:
            raise HTTPException(status_code=400, detail="endTimeUtc must be after startTimeUtc")
        candles = self.candle_service.ensure_candles(db, market_code=payload.market_code, timeframe=payload.timeframe, start_time_utc=payload.start_time_utc, end_time_utc=payload.end_time_utc)
        if len(candles) <= payload.initial_visible_count:
            raise HTTPException(status_code=400, detail="not enough candles for requested initialVisibleCount")
        session = TrainingSession(
            market_code=payload.market_code,
            timeframe=payload.timeframe,
            start_time_utc=payload.start_time_utc,
            end_time_utc=payload.end_time_utc,
            initial_visible_count=payload.initial_visible_count,
            current_index=payload.initial_visible_count - 1,
            total_candle_count=len(candles),
            initial_capital=payload.initial_capital,
            fee_rate=payload.fee_rate,
            cash=payload.initial_capital,
            position_qty=Decimal(0),
            avg_entry_price=Decimal(0),
            realized_pnl=Decimal(0),
            status=TrainingSessionStatus.running,
            mode=TrainingSessionMode.personal_review,
        )
        db.add(session)
        db.flush()
        self._save_equity_snapshot(db, session, candles[session.current_index])
        db.commit()
        db.refresh(session)
        return self.get_state(db, session.id)

    def get_state(self, db: Session, session_id: UUID) -> TrainingSessionState:
        session = self._require_session(db, session_id)
        if session.status == TrainingSessionStatus.finished:
            raise HTTPException(status_code=409, detail="session is finished; use review endpoint")
        return self._build_state(db, session)

    def next_candle(self, db: Session, session_id: UUID) -> TrainingSessionState:
        session = self._require_session(db, session_id, for_update=True)
        self._require_running(session)
        if session.current_index >= session.total_candle_count - 1:
            raise HTTPException(status_code=400, detail="cannot advance beyond final candle")
        session.current_index += 1
        candle = self._candles(db, session)[session.current_index]
        self._save_equity_snapshot(db, session, candle)
        db.commit()
        db.refresh(session)
        return self._build_state(db, session)

    def trade(self, db: Session, session_id: UUID, payload: TradeCreate) -> TrainingSessionState:
        session = self._require_session(db, session_id, for_update=True)
        self._require_running(session)
        candles = self._candles(db, session)
        candle = candles[session.current_index]
        if payload.side == TradeSide.buy:
            result = calculate_buy_order(cash=session.cash, position_qty=session.position_qty, avg_entry_price=session.avg_entry_price, price=candle.close, percentage=payload.percentage, fee_rate=session.fee_rate)
            realized_pnl = None
        else:
            result = calculate_sell_order(cash=session.cash, position_qty=session.position_qty, avg_entry_price=session.avg_entry_price, price=candle.close, percentage=payload.percentage, fee_rate=session.fee_rate)
            realized_pnl = result.realized_pnl
            session.realized_pnl += result.realized_pnl
        session.cash = result.cash_after
        session.position_qty = result.position_qty_after
        session.avg_entry_price = result.avg_entry_price_after
        trade = Trade(session_id=session.id, side=payload.side, candle_time_utc=candle.candle_time_utc, price=candle.close, quantity=result.quantity, gross_amount=result.gross_amount, fee=result.fee, net_amount=result.net_amount, realized_pnl=realized_pnl, cash_after=session.cash, position_qty_after=session.position_qty, avg_entry_price_after=session.avg_entry_price, note=payload.note, created_at=_now())
        db.add(trade)
        self._save_equity_snapshot(db, session, candle)
        db.commit()
        db.refresh(session)
        return self._build_state(db, session)

    def finish(self, db: Session, session_id: UUID) -> TrainingSession:
        session = self._require_session(db, session_id, for_update=True)
        self._require_running(session)
        candle = self._candles(db, session)[session.current_index]
        self._save_equity_snapshot(db, session, candle)
        session.status = TrainingSessionStatus.finished
        session.finished_at = _now()
        db.commit()
        db.refresh(session)
        return session

    def _require_session(self, db: Session, session_id: UUID, *, for_update: bool = False) -> TrainingSession:
        session = get_session(db, session_id, for_update=for_update)
        if session is None:
            raise HTTPException(status_code=404, detail="session not found")
        return session

    def _require_running(self, session: TrainingSession) -> None:
        if session.status != TrainingSessionStatus.running:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="session is not running")

    def _candles(self, db: Session, session: TrainingSession):
        return list_candles(db, market_code=session.market_code, timeframe=session.timeframe, start_time_utc=session.start_time_utc, end_time_utc=session.end_time_utc)

    def _visible_candles(self, db: Session, session: TrainingSession):
        return self._candles(db, session)[: session.current_index + 1]

    def _save_equity_snapshot(self, db: Session, session: TrainingSession, candle) -> None:
        equity = calculate_equity(cash=session.cash, position_qty=session.position_qty, current_price=candle.close)
        existing = list_equity_snapshots(db, session.id)
        peak = max([snapshot.equity for snapshot in existing] + [session.initial_capital, equity])
        snapshot = db.scalar(select(EquitySnapshot).where(EquitySnapshot.session_id == session.id, EquitySnapshot.candle_index == session.current_index))
        if snapshot is None:
            snapshot = EquitySnapshot(session_id=session.id, candle_time_utc=candle.candle_time_utc, candle_index=session.current_index, cash=session.cash, position_qty=session.position_qty, current_price=candle.close, equity=equity, drawdown=calculate_drawdown(equity=equity, peak_equity=peak), created_at=_now())
            db.add(snapshot)
            return
        snapshot.cash = session.cash
        snapshot.position_qty = session.position_qty
        snapshot.current_price = candle.close
        snapshot.equity = equity
        snapshot.drawdown = calculate_drawdown(equity=equity, peak_equity=peak)

    def _account_summary(self, db: Session, session: TrainingSession, current_price: Decimal) -> AccountSummary:
        equity = calculate_equity(cash=session.cash, position_qty=session.position_qty, current_price=current_price)
        snapshots = list_equity_snapshots(db, session.id)
        max_drawdown = max([snapshot.drawdown for snapshot in snapshots], default=Decimal(0))
        unrealized_pnl = (current_price - session.avg_entry_price) * session.position_qty if session.position_qty > 0 else Decimal(0)
        return AccountSummary(initial_capital=session.initial_capital, cash=session.cash, position_qty=session.position_qty, avg_entry_price=session.avg_entry_price, current_price=current_price, realized_pnl=session.realized_pnl, unrealized_pnl=unrealized_pnl, total_equity=equity, return_pct=calculate_return_pct(equity=equity, initial_capital=session.initial_capital), max_drawdown=max_drawdown)

    def _build_state(self, db: Session, session: TrainingSession) -> TrainingSessionState:
        visible_candles = self._visible_candles(db, session)
        current_price = visible_candles[-1].close
        return TrainingSessionState(session=session, visible_candles=visible_candles, trades=list_trades(db, session.id), account_summary=self._account_summary(db, session, current_price))
