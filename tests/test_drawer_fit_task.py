"""Tests for drawer-fit invoke task."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from invoke import MockContext

from gridfinity_invoke import projects


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for output files with isolated project state."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        # Create isolated project state (no active project)
        active_file = tmpdir_path / ".gridfinity-active"
        projects_dir = tmpdir_path / "projects"
        with patch.object(projects, "PROJECTS_DIR", projects_dir):
            with patch.object(projects, "ACTIVE_FILE", active_file):
                yield tmpdir_path


@pytest.fixture
def temp_project_dir():
    """Create a temporary directory for project tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        active_file = tmpdir_path / ".gridfinity-active"
        projects_dir = tmpdir_path / "projects"
        with patch.object(projects, "PROJECTS_DIR", projects_dir):
            with patch.object(projects, "ACTIVE_FILE", active_file):
                yield tmpdir_path


def test_drawer_fit_accepts_width_and_depth_parameters(temp_output_dir: Path) -> None:
    """Test task accepts --width and --depth parameters."""
    from tasks import drawer_fit

    ctx = MockContext()
    output_path = str(temp_output_dir / "drawer-fit")

    # Should not raise - accepts width and depth as float parameters
    drawer_fit(ctx, width=200.0, depth=200.0, output=output_path)

    # Verify files were created
    assert (temp_output_dir / "drawer-fit-baseplate.stl").exists()


def test_drawer_fit_displays_calculation_summary(
    temp_output_dir: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test task displays calculation summary."""
    from tasks import drawer_fit

    ctx = MockContext()
    output_path = str(temp_output_dir / "drawer-fit")

    drawer_fit(ctx, width=200.0, depth=200.0, output=output_path)

    captured = capsys.readouterr()

    # Check summary output contains key information
    assert "200" in captured.out  # Input dimensions
    assert "4" in captured.out  # Units (200/42 = 4)
    assert "168" in captured.out  # Actual mm (4*42 = 168)
    # Gap (32mm total or 16mm per side)
    assert "32" in captured.out or "16" in captured.out


def test_drawer_fit_outputs_warning_for_oversized_baseplate(
    temp_output_dir: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test task outputs warning when baseplate exceeds max units."""
    from tasks import drawer_fit

    ctx = MockContext()
    output_path = str(temp_output_dir / "drawer-fit")

    # Use dimensions that exceed max units (default 5x5)
    # 300mm / 42mm = 7 units, which exceeds MAX_GRIDFINITY_UNITS_X/Y (5)
    drawer_fit(ctx, width=300.0, depth=300.0, output=output_path)

    captured = capsys.readouterr()

    # Check warning is displayed
    assert "Warning" in captured.out or "warning" in captured.out.lower()
    # Should mention exceeds or split
    assert "exceed" in captured.out.lower() or "split" in captured.out.lower()


def test_drawer_fit_generates_stl_files(temp_output_dir: Path) -> None:
    """Test task generates both STL files in correct location."""
    from tasks import drawer_fit

    ctx = MockContext()
    output_path = str(temp_output_dir / "drawer-fit")

    # Use dimensions with significant gaps to trigger spacer generation
    drawer_fit(ctx, width=200.0, depth=200.0, output=output_path)

    # Verify baseplate file was created
    baseplate_path = temp_output_dir / "drawer-fit-baseplate.stl"
    assert baseplate_path.exists()
    assert baseplate_path.stat().st_size > 0


def test_drawer_fit_fails_for_invalid_dimensions(
    temp_output_dir: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test task fails with error for invalid dimensions (< 42mm)."""
    from tasks import drawer_fit

    ctx = MockContext()
    output_path = str(temp_output_dir / "drawer-fit")

    # Test width too small
    with pytest.raises(SystemExit) as exc_info:
        drawer_fit(ctx, width=30.0, depth=200.0, output=output_path)
    assert exc_info.value.code == 1

    captured = capsys.readouterr()
    assert "42" in captured.out.lower() or "minimum" in captured.out.lower()


def test_drawer_fit_fails_for_negative_dimensions(
    temp_output_dir: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test task fails with error for negative dimensions."""
    from tasks import drawer_fit

    ctx = MockContext()
    output_path = str(temp_output_dir / "drawer-fit")

    # Test negative width
    with pytest.raises(SystemExit) as exc_info:
        drawer_fit(ctx, width=-100.0, depth=200.0, output=output_path)
    assert exc_info.value.code == 1

    captured = capsys.readouterr()
    assert "positive" in captured.out.lower() or "42" in captured.out.lower()
