"""Tests for tool configuration validation."""

import subprocess
import sys


def test_ruff_can_lint_source_directory() -> None:
    """Test that ruff can lint the source directory without config errors."""
    result = subprocess.run(
        ["ruff", "check", "src/", "tests/"],
        capture_output=True,
        text=True,
    )
    # Exit code 0 means no issues, exit code 1 means lint issues found
    # Both are acceptable - we just want to verify ruff runs without config errors
    # Exit code 2 would indicate a configuration error
    assert result.returncode in (0, 1), (
        f"Ruff failed with config error (exit code {result.returncode}):\n"
        f"stderr: {result.stderr}"
    )


def test_mypy_can_typecheck_source_directory() -> None:
    """Test that mypy can type-check the source directory without config errors."""
    result = subprocess.run(
        ["mypy", "src/"],
        capture_output=True,
        text=True,
    )
    # Exit code 0 means no type errors, exit code 1 means type errors found
    # Both are acceptable - we just want to verify mypy runs without config errors
    # Exit code 2 would indicate a configuration/fatal error
    assert result.returncode in (0, 1), (
        f"Mypy failed with config error (exit code {result.returncode}):\n"
        f"stderr: {result.stderr}"
    )


def test_pyrefly_can_typecheck_source_directory() -> None:
    """Test that pyrefly can type-check the source directory without config errors."""
    result = subprocess.run(
        [sys.executable, "-m", "pyrefly", "check", "src/"],
        capture_output=True,
        text=True,
    )
    # Exit code 0 means no type errors
    # We want to verify pyrefly runs without config errors
    assert result.returncode == 0, (
        f"Pyrefly failed (exit code {result.returncode}):\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )


def test_ruff_format_can_check_source_directory() -> None:
    """Test that ruff format can check the source directory without config errors."""
    result = subprocess.run(
        ["ruff", "format", "--check", "src/", "tests/"],
        capture_output=True,
        text=True,
    )
    # Exit code 0 means formatted, exit code 1 means needs formatting
    # Both are acceptable - we verify ruff format runs without config errors
    assert result.returncode in (0, 1), (
        f"Ruff format failed with config error (exit code {result.returncode}):\n"
        f"stderr: {result.stderr}"
    )
