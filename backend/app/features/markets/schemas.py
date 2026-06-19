from app.core.schemas import CamelModel


class MarketRead(CamelModel):
    code: str
    base_currency: str
    quote_currency: str
    is_active: bool


class MarketsResponse(CamelModel):
    markets: list[MarketRead]
