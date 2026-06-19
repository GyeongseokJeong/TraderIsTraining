from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.features.candles.enums import Timeframe
from app.features.candles.schemas import CandlesResponse
from app.features.candles.service import CandleService

router = APIRouter(prefix="/candles", tags=["candles"])


@router.get("", response_model=CandlesResponse)
def get_candles(
    market_code: str = Query(alias="marketCode"),
    timeframe: Timeframe = Query(),
    start_time_utc: datetime = Query(alias="from"),
    end_time_utc: datetime = Query(alias="to"),
    db: Session = Depends(get_db),
) -> CandlesResponse:
    candles = CandleService().ensure_candles(db, market_code=market_code, timeframe=timeframe, start_time_utc=start_time_utc, end_time_utc=end_time_utc)
    return CandlesResponse(candles=candles)
