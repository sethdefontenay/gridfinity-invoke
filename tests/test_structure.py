"""Tests for project structure validation."""

import re
from pathlib import Path


def test_init_file_exists_with_version() -> None:
    """Test that __init__.py exists and contains __version__."""
    init_path = (
        Path(__file__).parent.parent / "src" / "gridfinity_invoke" / "__init__.py"
    )
    assert init_path.exists(), f"Expected {init_path} to exist"

    content = init_path.read_text()
    assert "__version__" in content, "__init__.py must define __version__"


def test_package_can_be_imported() -> None:
    """Test that gridfinity_invoke can be imported."""
    import gridfinity_invoke

    assert hasattr(gridfinity_invoke, "__version__")


def test_version_is_valid_semver() -> None:
    """Test that package version is a valid semver string."""
    from gridfinity_invoke import __version__

    # Basic semver pattern: MAJOR.MINOR.PATCH with optional pre-release
    semver_pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$"
    assert re.match(semver_pattern, __version__), (
        f"Version '{__version__}' is not a valid semver string"
    )
