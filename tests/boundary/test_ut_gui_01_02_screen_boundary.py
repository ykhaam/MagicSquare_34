"""Screen ECB wiring — UT-GUI-01~02 (UIBoundary injection, no Control import)."""

from __future__ import annotations

import ast
from pathlib import Path
from unittest.mock import Mock

import pytest

from boundary.schemas import ErrorResponse
from boundary.ui_boundary import UIBoundary
from tests.entity.conftest import G1_RD01

_MAIN_WINDOW_PATH = (
    Path(__file__).resolve().parents[2] / "src" / "boundary" / "screen" / "main_window.py"
)


class TestUtGui01ScreenBoundaryWiring:
    """UT-GUI-01/02 — Screen uses injected UIBoundary; ECB import direction."""

    def test_ut_gui_01_main_window_requires_uiboundary_parameter(self) -> None:
        """UT-GUI-01 — constructor exposes boundary dependency injection."""
        pytest.importorskip("PyQt6.QtWidgets")
        from PyQt6.QtWidgets import QApplication

        from boundary.screen.main_window import MagicSquareWindow

        app = QApplication.instance() or QApplication([])
        mock_boundary = Mock(spec=UIBoundary)
        mock_boundary.solve.return_value = [2, 2, 7, 3, 3, 10]

        window = MagicSquareWindow(boundary=mock_boundary)
        window._set_grid(G1_RD01)
        window._on_solve_clicked()

        mock_boundary.solve.assert_called_once()
        _ = app

    def test_ut_gui_02_main_window_module_does_not_import_control(self) -> None:
        """UT-GUI-02 — Screen layer must not import Control directly."""
        source = _MAIN_WINDOW_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        assert "control" not in imported

    def test_ut_gui_01_solve_shows_boundary_error_response(self) -> None:
        """UT-GUI-01 — ErrorResponse from Boundary is shown without Control."""
        pytest.importorskip("PyQt6.QtWidgets")
        from PyQt6.QtWidgets import QApplication

        from boundary.screen.main_window import MagicSquareWindow

        app = QApplication.instance() or QApplication([])
        mock_boundary = Mock(spec=UIBoundary)
        mock_boundary.solve.return_value = ErrorResponse(
            code="UI_INVALID_EMPTY_COUNT",
            message="Grid must contain exactly 2 empty cells (0).",
        )

        window = MagicSquareWindow(boundary=mock_boundary)
        window._set_grid(G1_RD01)
        window._on_solve_clicked()

        assert "UI_INVALID_EMPTY_COUNT" in window._result_label.text()
        _ = app
