"""Main window for the MagicSquare PyQt6 desktop UI."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
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
from boundary.error_codes import (
    UI_INTERNAL_CONTRACT_CODE,
    UI_INTERNAL_CONTRACT_MESSAGE,
)
from boundary.schemas import ErrorResponse
from boundary.screen.constants import (
    GRID_DIMENSION,
    SAMPLE_PUZZLE,
    STATUS_CLEARED,
    STATUS_READY,
    STATUS_SOLVED,
    STATUS_VALIDATION_FAILED,
    STYLE_CELL_DEFAULT,
    STYLE_CELL_FILLED,
    STYLE_DEFAULT,
    STYLE_ERROR,
    STYLE_SUCCESS,
    WINDOW_TITLE,
)
from control.puzzle_solver import solution
from entity.constants import EMPTY_CELL_VALUE, MAX_CELL_VALUE, MIN_CELL_VALUE


class MagicSquareWindow(QMainWindow):
    """Main window with a 4×4 grid editor and Boundary-backed solve action."""

    def __init__(self) -> None:
        """Build widgets and wire Boundary solve handler."""
        super().__init__()
        self._boundary = MagicSquareBoundary(resolve=solution)
        self._cells: list[list[QSpinBox]] = []
        self._status_label = QLabel(STATUS_READY)
        self._result_label = QLabel("")
        self._result_label.setWordWrap(True)
        self._init_ui()

    def _init_ui(self) -> None:
        """Lay out grid, controls, and status area."""
        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(480, 460)

        central = QWidget()
        root = QVBoxLayout(central)
        root.setSpacing(12)

        intro = QLabel(
            "Fill the magic square puzzle. Values 1-16 once each; "
            "use 0 for empty cells (exactly two)."
        )
        intro.setWordWrap(True)

        grid_group = QGroupBox("4x4 Grid")
        grid_layout = QGridLayout(grid_group)
        grid_layout.setHorizontalSpacing(6)
        grid_layout.setVerticalSpacing(6)

        corner = QLabel("")
        corner.setFixedWidth(24)
        grid_layout.addWidget(corner, 0, 0)
        for col in range(GRID_DIMENSION):
            header = QLabel(str(col + 1))
            header.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header.setStyleSheet("font-weight: 600; color: #566573;")
            grid_layout.addWidget(header, 0, col + 1)

        for row in range(GRID_DIMENSION):
            row_label = QLabel(str(row + 1))
            row_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row_label.setStyleSheet("font-weight: 600; color: #566573;")
            grid_layout.addWidget(row_label, row + 1, 0)

            row_cells: list[QSpinBox] = []
            for col in range(GRID_DIMENSION):
                spin = QSpinBox()
                spin.setRange(EMPTY_CELL_VALUE, MAX_CELL_VALUE)
                spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
                spin.setSpecialValueText("·")
                spin.setMinimumWidth(52)
                spin.setMinimumHeight(36)
                grid_layout.addWidget(spin, row + 1, col + 1)
                row_cells.append(spin)
            self._cells.append(row_cells)

        button_row = QHBoxLayout()
        solve_button = QPushButton("Solve")
        solve_button.setMinimumHeight(34)
        solve_button.clicked.connect(self._on_solve_clicked)

        sample_button = QPushButton("Load sample")
        sample_button.setMinimumHeight(34)
        sample_button.clicked.connect(self._on_sample_clicked)

        clear_button = QPushButton("Clear")
        clear_button.setMinimumHeight(34)
        clear_button.clicked.connect(self._on_clear_clicked)

        button_row.addWidget(solve_button)
        button_row.addWidget(sample_button)
        button_row.addWidget(clear_button)
        button_row.addStretch()

        result_group = QGroupBox("Result")
        result_layout = QVBoxLayout(result_group)
        result_layout.addWidget(self._status_label)
        result_layout.addWidget(self._result_label)

        root.addWidget(intro)
        root.addWidget(grid_group)
        root.addLayout(button_row)
        root.addWidget(result_group)
        root.addStretch()
        self.setCentralWidget(central)
        self._apply_app_stylesheet()

    def _apply_app_stylesheet(self) -> None:
        """Apply a light, readable application theme."""
        self.setStyleSheet(
            """
            QMainWindow { background-color: #f4f6f7; }
            QGroupBox {
                font-weight: 600;
                border: 1px solid #d5d8dc;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px;
            }
            QPushButton {
                background-color: #2e86c1;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 6px 14px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #2874a6; }
            QPushButton:pressed { background-color: #1f618d; }
            QSpinBox {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 2px;
            }
            """
        )

    def _read_grid(self) -> list[list[int]]:
        """Read current spin box values as a 4×4 integer matrix."""
        return [
            [self._cells[row][col].value() for col in range(GRID_DIMENSION)]
            for row in range(GRID_DIMENSION)
        ]

    def _set_grid(self, grid: list[list[int]]) -> None:
        """Populate spin boxes from a 4×4 matrix."""
        for row in range(GRID_DIMENSION):
            for col in range(GRID_DIMENSION):
                self._cells[row][col].setValue(grid[row][col])
        self._reset_cell_highlights()

    def _clear_grid(self) -> None:
        """Reset all cells to empty."""
        for row in range(GRID_DIMENSION):
            for col in range(GRID_DIMENSION):
                self._cells[row][col].setValue(EMPTY_CELL_VALUE)
        self._reset_cell_highlights()

    def _reset_cell_highlights(self) -> None:
        """Remove solve highlights from all cells."""
        for row in range(GRID_DIMENSION):
            for col in range(GRID_DIMENSION):
                self._cells[row][col].setStyleSheet(STYLE_CELL_DEFAULT)

    def _highlight_solution_cells(self, payload: list[int]) -> None:
        """Highlight cells filled by the solver."""
        self._reset_cell_highlights()
        r1, c1, n1, r2, c2, n2 = payload
        self._cells[r1 - 1][c1 - 1].setValue(n1)
        self._cells[r2 - 1][c2 - 1].setValue(n2)
        self._cells[r1 - 1][c1 - 1].setStyleSheet(STYLE_CELL_FILLED)
        self._cells[r2 - 1][c2 - 1].setStyleSheet(STYLE_CELL_FILLED)

    def _show_error(self, code: str, message: str) -> None:
        """Display Boundary validation failure."""
        self._status_label.setText(STATUS_VALIDATION_FAILED)
        self._result_label.setStyleSheet(STYLE_ERROR)
        self._result_label.setText(f"[{code}] {message}")

    def _show_success(self, payload: list[int]) -> None:
        """Display solver success output and apply fills to the grid."""
        self._highlight_solution_cells(payload)
        self._status_label.setText(STATUS_SOLVED)
        self._result_label.setStyleSheet(STYLE_SUCCESS)
        r1, c1, n1, r2, c2, n2 = payload
        self._result_label.setText(
            f"Output: {payload}\n"
            f"→ ({r1},{c1}) = {n1},  ({r2},{c2}) = {n2}  "
            f"(1-indexed, values {MIN_CELL_VALUE}-{MAX_CELL_VALUE})"
        )

    def _reset_result_panel(self) -> None:
        """Clear result messaging."""
        self._status_label.setText(STATUS_READY)
        self._result_label.clear()
        self._result_label.setStyleSheet(STYLE_DEFAULT)

    def _on_sample_clicked(self) -> None:
        """Load the PRD RD-01 sample puzzle."""
        self._set_grid(SAMPLE_PUZZLE)
        self._reset_result_panel()
        self._status_label.setText("Sample puzzle loaded (PRD RD-01).")

    def _on_clear_clicked(self) -> None:
        """Handle Clear button."""
        self._clear_grid()
        self._reset_result_panel()
        self._status_label.setText(STATUS_CLEARED)

    def _on_solve_clicked(self) -> None:
        """Validate via Boundary and show error or solver result."""
        grid = self._read_grid()
        result = self._boundary.solve(grid)

        if isinstance(result, ErrorResponse):
            self._show_error(result.code, result.message)
            return

        if isinstance(result, list):
            self._show_success(result)
            return

        self._show_error(
            UI_INTERNAL_CONTRACT_CODE,
            UI_INTERNAL_CONTRACT_MESSAGE,
        )
