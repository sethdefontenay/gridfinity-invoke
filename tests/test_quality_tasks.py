"""Tests for quality invoke tasks (lint, format, test, check)."""

import subprocess


def test_lint_task_runs_ruff_and_returns_exit_code() -> None:
    """Test that lint task runs ruff and returns appropriate exit code."""
    result = subprocess.run(
        ["invoke", "dev.lint"],
        capture_output=True,
        text=True,
    )
    # Exit code 0 means lint passed, non-zero means lint issues found
    # We expect the current codebase to pass linting
    assert result.returncode == 0, (
        f"Lint task failed (exit code {result.returncode}):\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )


def test_format_task_check_flag_returns_appropriate_exit_code() -> None:
    """Test that format task with --check flag validates without modifying files."""
    result = subprocess.run(
        ["invoke", "dev.format", "--check"],
        capture_output=True,
        text=True,
    )
    # Exit code 0 means files are properly formatted
    # Exit code 1 means files need formatting
    assert result.returncode in (0, 1), (
        f"Format --check task failed unexpectedly (exit code {result.returncode}):\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )
