import app.db.session  # noqa: F401
from app.db.base import Base


def test_session_import_registers_required_tables() -> None:
    required_tables = {"users", "training_sessions", "trades", "equity_snapshots"}

    assert required_tables.issubset(Base.metadata.tables.keys())
