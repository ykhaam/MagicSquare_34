"""Approve-pattern helpers for GM-1 golden master regression."""

from __future__ import annotations

import difflib
import re
from collections.abc import Callable, Sequence
from pathlib import Path

from boundary.schemas import ErrorResponse

from tests.golden_master.scenarios import GM2_SCENARIOS, GoldenMasterScenario

SECTION_SEPARATOR = "________________________________________"
SECTION_HEADER_PATTERN = re.compile(r"^\[(?P<name>[a-z_]+)\]$", re.MULTILINE)


def format_grid(grid: Sequence[Sequence[int]]) -> str:
    """Render a 4×4 grid as space-separated rows for the baseline file."""
    return "\n".join(" ".join(str(cell) for cell in row) for row in grid)


def serialize_result(result: list[int] | ErrorResponse) -> tuple[str, str]:
    """Map a Boundary solve result to an Output or Error block label and body."""
    if isinstance(result, list):
        return "Output", repr(result)
    return "Error", result.code


def format_scenario_block(
    section: str,
    grid: Sequence[Sequence[int]],
    result: list[int] | ErrorResponse,
) -> str:
    """Format one golden master section."""
    label, body = serialize_result(result)
    lines = [
        f"[{section}]",
        "Input:",
        format_grid(grid),
        f"{label}:",
        body,
    ]
    return "\n".join(lines)


def build_golden_master_content(
    solve: Callable[[list[list[int]]], list[int] | ErrorResponse],
    scenarios: Sequence[GoldenMasterScenario] = GM2_SCENARIOS,
) -> str:
    """Run all scenarios and assemble the full baseline file body."""
    blocks = [
        format_scenario_block(scenario.section, scenario.grid, solve(scenario.grid))
        for scenario in scenarios
    ]
    return f"\n{SECTION_SEPARATOR}\n\n".join(blocks) + "\n"


def parse_golden_master(content: str) -> dict[str, str]:
    """Parse section name → raw block text (without trailing separator)."""
    matches = list(SECTION_HEADER_PATTERN.finditer(content))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        name = match.group("name")
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        block = content[start:end].strip()
        if block.endswith(SECTION_SEPARATOR):
            block = block[: -len(SECTION_SEPARATOR)].strip()
        sections[name] = block
    return sections


def unified_diff(expected: str, actual: str, path: Path) -> str:
    """Return a unified diff string for pytest failure output."""
    diff_lines = difflib.unified_diff(
        expected.splitlines(keepends=True),
        actual.splitlines(keepends=True),
        fromfile="expected",
        tofile="actual",
        lineterm="",
    )
    body = "".join(diff_lines)
    if body:
        return body
    return (
        "--- expected\n"
        f"+++ actual ({path.name})\n"
        "@@ content mismatch @@\n"
    )


def approve_section(
    section: str,
    actual_block: str,
    expected_path: Path,
    full_content: str,
    *,
    auto_create: bool = True,
) -> str | None:
    """Approve one scenario block against the committed baseline file.

    Args:
        section: Section key (e.g. ``normal_success``).
        actual_block: Fresh formatted block for this scenario.
        expected_path: Path to ``golden_master_expected.txt``.
        full_content: Entire baseline body used when creating a missing file.
        auto_create: Write baseline when the file is absent.

    Returns:
        ``None`` on match; otherwise a failure message or unified diff.
    """
    if not expected_path.is_file():
        if not auto_create:
            return f"Golden master baseline missing: {expected_path}"
        expected_path.parent.mkdir(parents=True, exist_ok=True)
        expected_path.write_text(full_content, encoding="utf-8")
        return (
            f"Golden master baseline created at {expected_path}. "
            "Review the file and commit it, then re-run the test."
        )

    expected_sections = parse_golden_master(expected_path.read_text(encoding="utf-8"))
    expected_block = expected_sections.get(section)
    if expected_block is None:
        return f"Section [{section}] missing in {expected_path.name}"

    if expected_block == actual_block:
        return None

    return unified_diff(expected_block, actual_block, expected_path)


def approve_golden_master(
    actual: str,
    expected_path: Path,
    *,
    auto_create: bool = True,
) -> str | None:
    """Compare actual content with the baseline file using the approve pattern.

    Args:
        actual: Fresh solver output formatted as the golden master file body.
        expected_path: Path to the committed baseline file.
        auto_create: When True, write ``actual`` if the baseline file is missing.

    Returns:
        ``None`` when content matches. Otherwise a human-readable failure reason
        (missing baseline created, or unified diff for mismatch).
    """
    if not expected_path.is_file():
        if not auto_create:
            return f"Golden master baseline missing: {expected_path}"
        expected_path.parent.mkdir(parents=True, exist_ok=True)
        expected_path.write_text(actual, encoding="utf-8")
        return (
            f"Golden master baseline created at {expected_path}. "
            "Review the file and commit it, then re-run the test."
        )

    expected = expected_path.read_text(encoding="utf-8")
    if expected == actual:
        return None

    return unified_diff(expected, actual, expected_path)
