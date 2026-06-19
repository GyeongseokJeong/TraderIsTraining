from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.features.markets.repository import list_active_markets
from app.features.markets.schemas import MarketsResponse

router = APIRouter(prefix="/markets", tags=["markets"])


@router.get("", response_model=MarketsResponse)
def get_markets(db: Session = Depends(get_db)) -> MarketsResponse:
    return MarketsResponse(markets=list_active_markets(db))
