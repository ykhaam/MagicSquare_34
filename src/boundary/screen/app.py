"""PyQt6 desktop UI for MagicSquare Boundary solve flow."""

from __future__ import annotations

import sys
from typing import Final

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from boundary.magic_square_boundary import MagicSquareBoundary
from boundary.schemas import ErrorResponse
from control.puzzle_solver import solution

GRID_DIMENSION: Final[int] = 4
CELL_MIN_VALUE: Final[int] = 0
CELL_MAX_VALUE: Final[int] = 16
WINDOW_TITLE: Final[str] = "MagicSquare — 4×4 Puzzle"


class MagicSquareWindow(QMainWindow):
    """Main window with a 4×4 grid editor and Boundary-backed solve action."""

    def __init__(self) -> None:
        """Build widgets and wire Boundary solve handler."""
        super().__init__()
        self._boundary = MagicSquareBoundary(resolve=solution)
        self._cells: list[list[QSpinBox]] = []
        self._status_label = QLabel("Enter a 4×4 grid (0 = empty cell), then click Solve.")
        self._result_label = QLabel("")
        self._result_label.setWordWrap(True)
        self._init_ui()

    def _init_ui(self) -> None:
        """Lay out grid, controls, and status area."""
        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(420, 380)

        central = QWidget()
        root = QVBoxLayout(central)

        grid_group = QGroupBox("Grid (0 = empty)")
        grid_layout = QGridLayout(grid_group)
        for row in range(GRID_DIMENSION):
            row_cells: list[QSpinBox] = []
            for col in range(GRID_DIMENSION):
                spin = QSpinBox()
                spin.setRange(CELL_MIN_VALUE, CELL_MAX_VALUE)
                spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
                spin.setSpecialValueText("·")
                grid_layout.addWidget(spin, row, col)
                row_cells.append(spin)
            self._cells.append(row_cells)

        button_row = QHBoxLayout()
        solve_button = QPushButton("Solve")
        solve_button.clicked.connect(self._on_solve_clicked)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self._on_clear_clicked)
        button_row.addWidget(solve_button)
        button_row.addWidget(clear_button)
        button_row.addStretch()

        self._status_label.setObjectName("statusLabel")
        self._result_label.setObjectName("resultLabel")

        root.addWidget(grid_group)
        root.addLayout(button_row)
        root.addWidget(self._status_label)
        root.addWidget(self._result_label)
        root.addStretch()
        self.setCentralWidget(central)

    def _read_grid(self) -> list[list[int]]:
        """Read current spin box values as a 4×4 integer matrix."""
        return [
            [self._cells[row][col].value() for col in range(GRID_DIMENSION)]
            for row in range(GRID_DIMENSION)
        ]

    def _clear_grid(self) -> None:
        """Reset all cells to empty (0)."""
        for row in range(GRID_DIMENSION):
            for col in range(GRID_DIMENSION):
                self._cells[row][col].setValue(CELL_MIN_VALUE)

    def _show_error(self, code: str, message: str) -> None:
        """Display Boundary validation failure."""
        self._status_label.setText("Validation failed")
        self._result_label.setStyleSheet("color: #c0392b;")
        self._result_label.setText(f"[{code}] {message}")

    def _show_success(self, payload: list[int]) -> None:
        """Display solver success output."""
        self._status_label.setText("Solved")
        self._result_label.setStyleSheet("color: #27ae60;")
        self._result_label.setText(f"Result: {payload}")

    def _on_clear_clicked(self) -> None:
        """Handle Clear button."""
        self._clear_grid()
        self._status_label.setText("Grid cleared.")
        self._result_label.clear()

    def _on_solve_clicked(self) -> None:
        """Validate via Boundary and show error or solver result."""
        grid = self._read_grid()
        try:
            result = self._boundary.solve(grid)
        except Exception as exc:
            self._show_error("UI_INTERNAL", str(exc))
            return

        if isinstance(result, ErrorResponse):
            self._show_error(result.code, result.message)
            return

        if isinstance(result, list):
            self._show_success(result)
            return

        self._show_error("UI_INTERNAL", "Unexpected Boundary response type.")

    @staticmethod
    def load_sample_puzzle() -> list[list[int]]:
        """Return a sample partial grid for quick manual testing."""
        return [
            [16, 0, 3, 13],
            [5, 11, 10, 8],
            [9, 7, 6, 12],
            [4, 14, 0, 1],
        ]


def main() -> int:
    """Launch the MagicSquare PyQt6 application."""
    app = QApplication(sys.argv)
    window = MagicSquareWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
