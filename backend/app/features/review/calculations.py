from decimal import Decimal


def calculate_buy_and_hold_return(*, first_close: Decimal, final_close: Decimal) -> Decimal:
    if first_close <= 0:
        raise ValueError("first close must be positive")
    return ((final_close - first_close) / first_close) * Decimal(100)


def calculate_win_rate(realized_pnls: list[Decimal]) -> Decimal | None:
    if not realized_pnls:
        return None
    wins = sum(1 for value in realized_pnls if value > 0)
    return (Decimal(wins) / Decimal(len(realized_pnls))) * Decimal(100)


def calculate_profit_factor(realized_pnls: list[Decimal]) -> Decimal | None:
    gross_profit = sum((value for value in realized_pnls if value > 0), Decimal(0))
    gross_loss = sum((value for value in realized_pnls if value < 0), Decimal(0))
    if gross_loss == 0:
        return None
    return gross_profit / abs(gross_loss)


def calculate_average_win_loss(realized_pnls: list[Decimal]) -> tuple[Decimal | None, Decimal | None]:
    wins = [value for value in realized_pnls if value > 0]
    losses = [value for value in realized_pnls if value < 0]
    average_win = sum(wins, Decimal(0)) / Decimal(len(wins)) if wins else None
    average_loss = sum(losses, Decimal(0)) / Decimal(len(losses)) if losses else None
    return average_win, average_loss
