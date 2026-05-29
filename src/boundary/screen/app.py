"""Application entrypoint for the MagicSquare screen layer."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from boundary.screen.window import MagicSquareWindow


def main() -> int:
    """Launch the MagicSquare PyQt6 application."""
    app = QApplication(sys.argv)
    app.setApplicationName("MagicSquare")
    window = MagicSquareWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
