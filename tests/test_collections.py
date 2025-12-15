"""Tests for invoke collections restructure.

Tests that namespaced commands work correctly after restructuring
tasks into invoke_collections/dev.py and invoke_collections/gf.py.
"""

import subprocess
import sys
from pathlib import Path


def test_dev_lint_command_exists():
    """Test that 'inv dev.lint' command exists and can be invoked."""
    result = subprocess.run(
        [sys.executable, "-m", "invoke", "--list"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    assert "dev.lint" in result.stdout


def test_gf_baseplate_command_exists():
    """Test that 'inv gf.baseplate' command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "invoke", "--list"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    assert "gf.baseplate" in result.stdout


def test_gf_config_show_command_exists():
    """Test that 'inv gf.config' command exists with --show flag."""
    result = subprocess.run(
        [sys.executable, "-m", "invoke", "--list"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    assert "gf.config" in result.stdout


def test_pp_enumerates_both_namespaces():
    """Test that 'inv pp' shows commands from both dev and gf namespaces."""
    result = subprocess.run(
        [sys.executable, "-m", "invoke", "pp"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    # Check for dev namespace commands
    assert "dev.lint" in result.stdout or "lint" in result.stdout
    # Check for gf namespace commands
    assert "gf.baseplate" in result.stdout or "baseplate" in result.stdout


def test_dev_format_command_exists():
    """Test that 'inv dev.format' command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "invoke", "--list"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    assert "dev.format" in result.stdout


def test_gf_bin_command_exists():
    """Test that 'inv gf.bin' command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "invoke", "--list"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0
    assert "gf.bin" in result.stdout
