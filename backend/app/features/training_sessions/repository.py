from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.equity_snapshots.models import EquitySnapshot
from app.features.trades.models import Trade
from app.features.training_sessions.models import TrainingSession


def get_session(db: Session, session_id: UUID, *, for_update: bool = False) -> TrainingSession | None:
    stmt = select(TrainingSession).where(TrainingSession.id == session_id)
    if for_update:
        stmt = stmt.with_for_update()
    return db.scalar(stmt)


def list_trades(db: Session, session_id: UUID) -> list[Trade]:
    return list(db.scalars(select(Trade).where(Trade.session_id == session_id).order_by(Trade.created_at)).all())


def list_equity_snapshots(db: Session, session_id: UUID) -> list[EquitySnapshot]:
    return list(db.scalars(select(EquitySnapshot).where(EquitySnapshot.session_id == session_id).order_by(EquitySnapshot.candle_index)).all())
