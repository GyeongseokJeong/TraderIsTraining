from __future__ import annotations

import ast
from pathlib import Path

import app.db.session  # noqa: F401
from app.db.base import Base

FEATURES_DIR = Path(__file__).resolve().parents[2] / "features"


def test_session_import_registers_required_tables() -> None:
    required_tables = {"users", "training_sessions", "trades", "equity_snapshots"}

    assert required_tables.issubset(Base.metadata.tables.keys())


def _foreign_key_targets() -> dict[str, set[str]]:
    targets_by_model_file: dict[str, set[str]] = {}
    for model_file in FEATURES_DIR.rglob("*.py"):
        source = model_file.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(model_file))
        table_names = {
            node.value.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Assign)
            for target in node.targets
            if isinstance(target, ast.Name)
            and target.id == "__tablename__"
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        }
        foreign_key_tables = {
            arg.value.split(".", maxsplit=1)[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "ForeignKey"
            for arg in node.args[:1]
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str)
        }
        if foreign_key_tables:
            targets_by_model_file.update({table_name: foreign_key_tables for table_name in table_names})
    return targets_by_model_file


def test_db_models_registers_feature_models_with_foreign_keys_and_targets() -> None:
    tables = Base.metadata.tables.keys()

    for model_table, target_tables in _foreign_key_targets().items():
        assert model_table in tables
        assert target_tables.issubset(tables)
