from decimal import Decimal

import pytest

from app.features.review.calculations import (
    calculate_buy_and_hold_return,
    calculate_profit_factor,
    calculate_win_rate,
)
from app.features.training_sessions.calculations import (
    calculate_buy_order,
    calculate_equity,
    calculate_sell_order,
)


def test_buy_order_fee_and_average_price() -> None:
    result = calculate_buy_order(cash=Decimal("1000000"), position_qty=Decimal("0"), avg_entry_price=Decimal("0"), price=Decimal("100000"), percentage=100, fee_rate=Decimal("0.0005"))
    assert result.net_amount == Decimal("1000000")
    assert result.fee > 0
    assert result.quantity > 0
    assert result.avg_entry_price_after == Decimal("100000")


def test_multiple_buys_update_average_entry_price() -> None:
    first = calculate_buy_order(cash=Decimal("1000000"), position_qty=Decimal("0"), avg_entry_price=Decimal("0"), price=Decimal("100"), percentage=50, fee_rate=Decimal("0"))
    second = calculate_buy_order(cash=first.cash_after, position_qty=first.position_qty_after, avg_entry_price=first.avg_entry_price_after, price=Decimal("200"), percentage=100, fee_rate=Decimal("0"))
    assert second.avg_entry_price_after == Decimal("133.3333333333333333333333333")


def test_partial_sell_realized_pnl_and_avg_price_unchanged() -> None:
    result = calculate_sell_order(cash=Decimal("0"), position_qty=Decimal("10"), avg_entry_price=Decimal("100"), price=Decimal("120"), percentage=50, fee_rate=Decimal("0.0005"))
    assert result.quantity == Decimal("5")
    assert result.realized_pnl == Decimal("99.7000")
    assert result.avg_entry_price_after == Decimal("100")


def test_full_sell_resets_position() -> None:
    result = calculate_sell_order(cash=Decimal("0"), position_qty=Decimal("10"), avg_entry_price=Decimal("100"), price=Decimal("100"), percentage=100, fee_rate=Decimal("0"))
    assert result.position_qty_after == Decimal("0")
    assert result.avg_entry_price_after == Decimal("0")


def test_prevent_sell_without_position() -> None:
    with pytest.raises(ValueError):
        calculate_sell_order(cash=Decimal("0"), position_qty=Decimal("0"), avg_entry_price=Decimal("0"), price=Decimal("100"), percentage=25, fee_rate=Decimal("0"))


def test_prevent_buy_without_cash() -> None:
    with pytest.raises(ValueError):
        calculate_buy_order(cash=Decimal("0"), position_qty=Decimal("0"), avg_entry_price=Decimal("0"), price=Decimal("100"), percentage=25, fee_rate=Decimal("0"))


def test_equity_and_review_metrics() -> None:
    assert calculate_equity(cash=Decimal("100"), position_qty=Decimal("2"), current_price=Decimal("50")) == Decimal("200")
    assert calculate_buy_and_hold_return(first_close=Decimal("100"), final_close=Decimal("125")) == Decimal("25.00")
    assert calculate_win_rate([Decimal("10"), Decimal("-5")]) == Decimal("50.0")
    assert calculate_profit_factor([Decimal("10"), Decimal("-5")]) == Decimal("2")
