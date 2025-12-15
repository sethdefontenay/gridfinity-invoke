"""Integration tests for inv gf.config command."""

import subprocess
import sys
from pathlib import Path


def test_config_command_requires_flag():
    """Test that 'inv gf.config' without flags shows error message."""
    result = subprocess.run(
        [sys.executable, "-m", "invoke", "gf.config"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )

    # Should exit with error code
    assert result.returncode != 0

    # Should show error message and usage hint
    output = result.stdout + result.stderr
    assert "Error" in output or "error" in output
    assert "--init" in output or "--show" in output


def test_config_show_command_displays_current_config():
    """Test that 'inv gf.config --show' displays configuration values."""
    # This test runs in the project context which may or may not have .gf-config
    result = subprocess.run(
        [sys.executable, "-m", "invoke", "gf.config", "--show"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )

    # Should succeed
    assert result.returncode == 0

    # Should display printer config information
    output = result.stdout.lower()
    assert "print bed" in output or "printer" in output
    assert "mm" in output  # Should show dimensions in mm
