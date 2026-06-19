from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class BuyOrderResult:
    quantity: Decimal
    gross_amount: Decimal
    fee: Decimal
    net_amount: Decimal
    cash_after: Decimal
    position_qty_after: Decimal
    avg_entry_price_after: Decimal


@dataclass(frozen=True)
class SellOrderResult:
    quantity: Decimal
    gross_amount: Decimal
    fee: Decimal
    net_amount: Decimal
    realized_pnl: Decimal
    cash_after: Decimal
    position_qty_after: Decimal
    avg_entry_price_after: Decimal


def _percentage_ratio(percentage: int) -> Decimal:
    if percentage not in {25, 50, 75, 100}:
        raise ValueError("percentage must be one of 25, 50, 75, 100")
    return Decimal(percentage) / Decimal(100)


def calculate_buy_order(
    *, cash: Decimal, position_qty: Decimal, avg_entry_price: Decimal, price: Decimal, percentage: int, fee_rate: Decimal
) -> BuyOrderResult:
    if cash <= 0:
        raise ValueError("cash is insufficient")
    if price <= 0:
        raise ValueError("price must be positive")
    ratio = _percentage_ratio(percentage)
    net_amount = cash * ratio
    if net_amount <= 0:
        raise ValueError("cash is insufficient")
    gross_amount = net_amount / (Decimal(1) + fee_rate)
    fee = net_amount - gross_amount
    quantity = gross_amount / price
    position_cost = position_qty * avg_entry_price
    position_qty_after = position_qty + quantity
    avg_entry_price_after = (position_cost + gross_amount) / position_qty_after
    return BuyOrderResult(quantity, gross_amount, fee, net_amount, cash - net_amount, position_qty_after, avg_entry_price_after)


def calculate_sell_order(
    *, cash: Decimal, position_qty: Decimal, avg_entry_price: Decimal, price: Decimal, percentage: int, fee_rate: Decimal
) -> SellOrderResult:
    if position_qty <= 0:
        raise ValueError("position is empty")
    if price <= 0:
        raise ValueError("price must be positive")
    ratio = _percentage_ratio(percentage)
    quantity = position_qty * ratio
    gross_amount = quantity * price
    fee = gross_amount * fee_rate
    net_amount = gross_amount - fee
    realized_pnl = (price - avg_entry_price) * quantity - fee
    position_qty_after = position_qty - quantity
    if position_qty_after.copy_abs() < Decimal("0.000000000000000001"):
        position_qty_after = Decimal(0)
    avg_entry_price_after = avg_entry_price if position_qty_after > 0 else Decimal(0)
    return SellOrderResult(quantity, gross_amount, fee, net_amount, realized_pnl, cash + net_amount, position_qty_after, avg_entry_price_after)


def calculate_equity(*, cash: Decimal, position_qty: Decimal, current_price: Decimal) -> Decimal:
    return cash + (position_qty * current_price)


def calculate_return_pct(*, equity: Decimal, initial_capital: Decimal) -> Decimal:
    if initial_capital <= 0:
        raise ValueError("initial capital must be positive")
    return ((equity - initial_capital) / initial_capital) * Decimal(100)


def calculate_drawdown(*, equity: Decimal, peak_equity: Decimal) -> Decimal:
    if peak_equity <= 0:
        return Decimal(0)
    return (peak_equity - equity) / peak_equity
