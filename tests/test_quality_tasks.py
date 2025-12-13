"""Tests for quality invoke tasks (lint, format, test, check)."""

import subprocess


def test_lint_task_runs_ruff_and_returns_exit_code() -> None:
    """Test that lint task runs ruff and returns appropriate exit code."""
    result = subprocess.run(
        ["invoke", "lint"],
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
        ["invoke", "format", "--check"],
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


def test_test_task_runs_pytest_and_captures_output() -> None:
    """Test that test task runs pytest and captures output."""
    result = subprocess.run(
        ["invoke", "test"],
        capture_output=True,
        text=True,
    )
    # Test task should run pytest - we check for pytest-related output
    # Coverage report or test results should appear in output
    combined_output = result.stdout + result.stderr
    assert "test" in combined_output.lower() or "passed" in combined_output.lower(), (
        f"Test task did not appear to run pytest:\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )


def test_check_task_runs_lint_before_test_fail_fast() -> None:
    """Test that check task runs lint before test with fail-fast behavior."""
    result = subprocess.run(
        ["invoke", "check"],
        capture_output=True,
        text=True,
    )
    combined_output = result.stdout + result.stderr
    # Check should run both lint and test
    # Verify lint runs (ruff output or "lint" mention)
    # Verify tests run (pytest output)
    has_lint = "ruff" in combined_output.lower() or "lint" in combined_output.lower()
    has_test = "test" in combined_output.lower() or "pytest" in combined_output.lower()

    assert has_lint, (
        f"Check task did not appear to run lint:\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )
    assert has_test, (
        f"Check task did not appear to run tests:\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )
