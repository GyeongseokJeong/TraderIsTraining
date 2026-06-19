"""seed supported markets

Revision ID: 0002_seed_supported_markets
Revises: 0001_create_base_tables
Create Date: 2026-06-19
"""
from collections.abc import Sequence

from alembic import op

revision: str = "0002_seed_supported_markets"
down_revision: str | None = "0001_create_base_tables"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.execute(
        """
        INSERT INTO markets (id, code, base_currency, quote_currency, is_active, created_at, updated_at)
        VALUES
          (gen_random_uuid(), 'KRW-BTC', 'BTC', 'KRW', true, now(), now()),
          (gen_random_uuid(), 'KRW-ETH', 'ETH', 'KRW', true, now(), now()),
          (gen_random_uuid(), 'KRW-XRP', 'XRP', 'KRW', true, now(), now()),
          (gen_random_uuid(), 'KRW-SOL', 'SOL', 'KRW', true, now(), now())
        ON CONFLICT (code) DO NOTHING
        """
    )


def downgrade() -> None:
    op.execute("DELETE FROM markets WHERE code IN ('KRW-BTC', 'KRW-ETH', 'KRW-XRP', 'KRW-SOL')")
