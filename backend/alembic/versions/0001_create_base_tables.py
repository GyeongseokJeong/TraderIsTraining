"""create base tables

Revision ID: 0001_create_base_tables
Revises:
Create Date: 2026-06-19
"""
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "0001_create_base_tables"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    timeframe = postgresql.ENUM("MINUTE_1", "MINUTE_5", "MINUTE_15", "MINUTE_60", "MINUTE_240", "DAY", name="timeframe", create_type=False)
    status = postgresql.ENUM("SETUP", "RUNNING", "FINISHED", name="training_session_status", create_type=False)
    mode = postgresql.ENUM("PERSONAL_REVIEW", name="training_session_mode", create_type=False)
    side = postgresql.ENUM("BUY", "SELL", name="trade_side", create_type=False)
    timeframe.create(op.get_bind(), checkfirst=True)
    status.create(op.get_bind(), checkfirst=True)
    mode.create(op.get_bind(), checkfirst=True)
    side.create(op.get_bind(), checkfirst=True)

    op.create_table("users", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("email", sa.String(255), nullable=True), sa.Column("display_name", sa.String(100), nullable=True), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_unique_constraint("uq_users_email", "users", ["email"])
    op.create_table("markets", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("code", sa.String(20), nullable=False), sa.Column("base_currency", sa.String(20), nullable=False), sa.Column("quote_currency", sa.String(20), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_markets_code", "markets", ["code"], unique=True)
    op.create_table("candles", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("market_code", sa.String(20), nullable=False), sa.Column("timeframe", timeframe, nullable=False), sa.Column("candle_time_utc", sa.DateTime(timezone=True), nullable=False), sa.Column("candle_time_kst", sa.DateTime(timezone=True), nullable=False), sa.Column("open", sa.Numeric(28, 10), nullable=False), sa.Column("high", sa.Numeric(28, 10), nullable=False), sa.Column("low", sa.Numeric(28, 10), nullable=False), sa.Column("close", sa.Numeric(28, 10), nullable=False), sa.Column("volume", sa.Numeric(38, 18), nullable=False), sa.Column("trade_price_volume", sa.Numeric(38, 10), nullable=True), sa.Column("source", sa.String(20), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False), sa.UniqueConstraint("market_code", "timeframe", "candle_time_utc", name="uq_candle_identity"))
    op.create_index("ix_candles_market_timeframe_time", "candles", ["market_code", "timeframe", "candle_time_utc"])
    op.create_table("training_sessions", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=True), sa.Column("market_code", sa.String(20), nullable=False), sa.Column("timeframe", timeframe, nullable=False), sa.Column("start_time_utc", sa.DateTime(timezone=True), nullable=False), sa.Column("end_time_utc", sa.DateTime(timezone=True), nullable=False), sa.Column("initial_visible_count", sa.Integer(), nullable=False), sa.Column("current_index", sa.Integer(), nullable=False), sa.Column("total_candle_count", sa.Integer(), nullable=False), sa.Column("initial_capital", sa.Numeric(28, 10), nullable=False), sa.Column("fee_rate", sa.Numeric(18, 10), nullable=False), sa.Column("cash", sa.Numeric(28, 10), nullable=False), sa.Column("position_qty", sa.Numeric(38, 18), nullable=False), sa.Column("avg_entry_price", sa.Numeric(28, 10), nullable=False), sa.Column("realized_pnl", sa.Numeric(28, 10), nullable=False), sa.Column("status", status, nullable=False), sa.Column("mode", mode, nullable=False), sa.Column("random_seed", sa.String(100), nullable=True), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False), sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True))
    op.create_index("ix_training_sessions_market_code", "training_sessions", ["market_code"])
    op.create_table("trades", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("session_id", sa.Uuid(), sa.ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False), sa.Column("side", side, nullable=False), sa.Column("candle_time_utc", sa.DateTime(timezone=True), nullable=False), sa.Column("price", sa.Numeric(28, 10), nullable=False), sa.Column("quantity", sa.Numeric(38, 18), nullable=False), sa.Column("gross_amount", sa.Numeric(28, 10), nullable=False), sa.Column("fee", sa.Numeric(28, 10), nullable=False), sa.Column("net_amount", sa.Numeric(28, 10), nullable=False), sa.Column("realized_pnl", sa.Numeric(28, 10), nullable=True), sa.Column("cash_after", sa.Numeric(28, 10), nullable=False), sa.Column("position_qty_after", sa.Numeric(38, 18), nullable=False), sa.Column("avg_entry_price_after", sa.Numeric(28, 10), nullable=False), sa.Column("note", sa.Text(), nullable=True), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_trades_session_id", "trades", ["session_id"])
    op.create_index("ix_trades_session_time", "trades", ["session_id", "candle_time_utc"])
    op.create_table("equity_snapshots", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("session_id", sa.Uuid(), sa.ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False), sa.Column("candle_time_utc", sa.DateTime(timezone=True), nullable=False), sa.Column("candle_index", sa.Integer(), nullable=False), sa.Column("cash", sa.Numeric(28, 10), nullable=False), sa.Column("position_qty", sa.Numeric(38, 18), nullable=False), sa.Column("current_price", sa.Numeric(28, 10), nullable=False), sa.Column("equity", sa.Numeric(28, 10), nullable=False), sa.Column("drawdown", sa.Numeric(18, 10), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.UniqueConstraint("session_id", "candle_index", name="uq_equity_snapshot_session_index"))
    op.create_index("ix_equity_snapshots_session_index", "equity_snapshots", ["session_id", "candle_index"])
    op.create_table("challenge_templates", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("market_code", sa.String(20), nullable=False), sa.Column("timeframe", timeframe, nullable=False), sa.Column("start_time_utc", sa.DateTime(timezone=True), nullable=False), sa.Column("end_time_utc", sa.DateTime(timezone=True), nullable=False), sa.Column("initial_capital", sa.Numeric(28, 10), nullable=False), sa.Column("fee_rate", sa.Numeric(18, 10), nullable=False), sa.Column("title", sa.String(200), nullable=False), sa.Column("description", sa.Text(), nullable=True), sa.Column("is_active", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))


def downgrade() -> None:
    op.drop_table("challenge_templates")
    op.drop_table("equity_snapshots")
    op.drop_table("trades")
    op.drop_table("training_sessions")
    op.drop_table("candles")
    op.drop_table("markets")
    op.drop_table("users")
    for enum_name in ["trade_side", "training_session_mode", "training_session_status", "timeframe"]:
        postgresql.ENUM(name=enum_name).drop(op.get_bind(), checkfirst=True)
