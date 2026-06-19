from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.markets.models import Market

SUPPORTED_MARKETS = {"KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-SOL"}


def list_active_markets(db: Session) -> list[Market]:
    return list(db.scalars(select(Market).where(Market.is_active.is_(True)).order_by(Market.code)).all())


def ensure_market_allowed(market_code: str) -> None:
    if market_code not in SUPPORTED_MARKETS:
        raise ValueError("unsupported market")
