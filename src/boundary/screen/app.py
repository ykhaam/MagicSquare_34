"""Application entrypoint for the MagicSquare screen layer."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from boundary.screen.main_window import MagicSquareWindow
from boundary.ui_boundary import UIBoundary
from control.solve_partial_magic_square import solution


def main() -> int:
    """Launch the MagicSquare PyQt6 application."""
    app = QApplication(sys.argv)
    app.setApplicationName("MagicSquare")
    boundary = UIBoundary(execute=solution)
    window = MagicSquareWindow(boundary=boundary)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
