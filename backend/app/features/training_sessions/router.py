from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.features.review.schemas import ReviewResponse
from app.features.review.service import ReviewService
from app.features.training_sessions.schemas import (
    TradeCreate,
    TrainingSessionCreate,
    TrainingSessionState,
)
from app.features.training_sessions.service import TrainingSessionService

router = APIRouter(prefix="/training-sessions", tags=["training-sessions"])


@router.post("", response_model=TrainingSessionState)
def create_training_session(payload: TrainingSessionCreate, db: Session = Depends(get_db)) -> TrainingSessionState:
    return TrainingSessionService().create_session(db, payload)


@router.get("/{session_id}", response_model=TrainingSessionState)
def get_training_session(session_id: UUID, db: Session = Depends(get_db)) -> TrainingSessionState:
    return TrainingSessionService().get_state(db, session_id)


@router.post("/{session_id}/next", response_model=TrainingSessionState)
def next_candle(session_id: UUID, db: Session = Depends(get_db)) -> TrainingSessionState:
    return TrainingSessionService().next_candle(db, session_id)


@router.post("/{session_id}/trade", response_model=TrainingSessionState)
def place_trade(session_id: UUID, payload: TradeCreate, db: Session = Depends(get_db)) -> TrainingSessionState:
    return TrainingSessionService().trade(db, session_id, payload)


@router.post("/{session_id}/finish", response_model=ReviewResponse)
def finish_session(session_id: UUID, db: Session = Depends(get_db)) -> ReviewResponse:
    TrainingSessionService().finish(db, session_id)
    return ReviewService().get_review(db, session_id)


@router.get("/{session_id}/review", response_model=ReviewResponse)
def get_review(session_id: UUID, db: Session = Depends(get_db)) -> ReviewResponse:
    return ReviewService().get_review(db, session_id)
