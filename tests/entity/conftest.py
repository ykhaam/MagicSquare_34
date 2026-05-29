"""Entity-track fixtures — G0~G3 placeholders (RED skeleton only)."""

from __future__ import annotations

# G0: complete magic square — D-VAL-01
# G0 = [
#     [16, 3, 2, 13],
#     [5, 10, 11, 8],
#     [9, 6, 7, 12],
#     [4, 15, 14, 1],
# ]

# G1: two blanks at (2,2),(3,3); missing {7,10} — D-LOC-01, D-MIS-01, D-SOL-01
# G1 = [
#     [16, 3, 2, 13],
#     [5, 0, 11, 8],
#     [9, 6, 0, 12],
#     [4, 15, 14, 1],
# ]

# G2: Step A fail / Step B success (PRD RD-02) — D-SOL-02 (TBD)
# G2 = [
#     [16, 0, 3, 13],
#     [5, 11, 10, 8],
#     [9, 7, 6, 12],
#     [4, 14, 15, 0],
# ]

# G3: unsolvable — D-SOL-03
# G3 = [
#     [34, 0, 0, 0],
#     [0, 0, 0, 34],
#     [0, 0, 34, 0],
#     [0, 34, 0, 0],
# ]

# G0-ROW / G0-COL / G0-DIAG / G0-DUP / G0-ZERO: D-VAL-02~06 variants (TBD)
