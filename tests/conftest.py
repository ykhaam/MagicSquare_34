"""Pytest configuration — ensure src layout is importable."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_SRC = Path(__file__).resolve().parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "golden_master: GM-2 Golden Master regression (approve pattern)",
    )
