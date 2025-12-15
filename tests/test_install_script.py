"""Tests for install.sh script."""

import os
from pathlib import Path


def test_install_script_exists_and_is_executable() -> None:
    """Test that install.sh script exists and has executable permissions."""
    script_path = Path(__file__).parent.parent / "install.sh"
    assert script_path.exists(), "install.sh does not exist in project root"
    assert os.access(script_path, os.X_OK), (
        "install.sh is not executable (missing +x permission)"
    )


def test_install_script_uses_bash_shebang() -> None:
    """Test that install.sh uses bash shebang."""
    script_path = Path(__file__).parent.parent / "install.sh"
    with open(script_path, "r") as f:
        first_line = f.readline().strip()
    assert first_line == "#!/bin/bash", (
        f"install.sh should use '#!/bin/bash' shebang, got: {first_line}"
    )


def test_install_script_sets_fail_fast_mode() -> None:
    """Test that install.sh sets fail-fast mode with 'set -e'."""
    script_path = Path(__file__).parent.parent / "install.sh"
    with open(script_path, "r") as f:
        content = f.read()
    # Check that 'set -e' appears early in the script (within first 10 lines)
    first_lines = "\n".join(content.split("\n")[:10])
    assert "set -e" in first_lines, (
        "install.sh should set fail-fast mode with 'set -e' near the top of the script"
    )
