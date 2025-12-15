"""Integration tests for drawer-fit feature.

These tests verify end-to-end workflows and critical integration points
for the drawer-fit feature.
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from invoke import MockContext

from gridfinity_invoke import config, projects


@pytest.fixture
def isolated_project_env():
    """Create a fully isolated environment for project-related tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        active_file = tmpdir_path / ".gridfinity-active"
        projects_dir = tmpdir_path / "projects"
        config_file = tmpdir_path / ".gf-config"
        # Create default config file to avoid prompting
        config_file.write_text(
            json.dumps(
                {
                    "print_bed_width_mm": 225,
                    "print_bed_depth_mm": 225,
                },
                indent=2,
            )
        )
        with patch.object(projects, "PROJECTS_DIR", projects_dir):
            with patch.object(projects, "ACTIVE_FILE", active_file):
                with patch.object(config, "CONFIG_FILE", config_file):
                    yield tmpdir_path


def test_exactly_42mm_produces_1x1_baseplate(isolated_project_env: Path) -> None:
    """Test edge case: exactly 42mm input produces 1x1 baseplate."""
    from gridfinity_invoke.generators import generate_drawer_fit

    tmpdir = isolated_project_env
    baseplate_path = tmpdir / "baseplate.stl"
    spacer_path = tmpdir / "spacers.stl"

    # Exactly 42mm should produce exactly 1 unit
    result = generate_drawer_fit(42.0, 42.0, baseplate_path, spacer_path)

    assert result.units_width == 1
    assert result.units_depth == 1
    assert result.actual_width_mm == 42.0
    assert result.actual_depth_mm == 42.0
    assert result.gap_x_mm == 0.0
    assert result.gap_y_mm == 0.0
    # No spacers should be generated (zero gap)
    assert result.spacer_path is None
    # Baseplate should exist
    assert result.baseplate_path.exists()


def test_project_workflow_drawer_fit_then_load_regenerates(
    isolated_project_env: Path,
) -> None:
    """Test project workflow: new-project -> drawer-fit -> load regenerates."""
    from invoke_collections.gf import drawer_fit, load, new_project

    ctx = MockContext()
    project_name = "load-test-project"

    # Step 1: Create new project
    new_project(ctx, name=project_name)

    # Step 2: Add drawer-fit component
    with patch("invoke_collections.gf.prompt_with_default", return_value="my-drawer"):
        drawer_fit(ctx, width=200.0, depth=150.0)

    # Verify files were created
    project_dir = isolated_project_env / "projects" / project_name
    baseplate_path = project_dir / "my-drawer-baseplate.stl"
    spacer_path = project_dir / "my-drawer-spacers.stl"

    assert baseplate_path.exists()
    # Note: spacers may or may not exist depending on gap size

    # Record original modification times
    baseplate_mtime_before = baseplate_path.stat().st_mtime

    # Step 3: Delete the STL files to simulate needing regeneration
    baseplate_path.unlink()
    if spacer_path.exists():
        spacer_path.unlink()

    # Step 4: Load project (should regenerate all STL files)
    load(ctx, project=project_name)

    # Step 5: Verify files were regenerated
    assert baseplate_path.exists()
    # Check that the file was actually recreated (new mtime)
    assert baseplate_path.stat().st_mtime > baseplate_mtime_before


def test_spacer_stl_created_with_sufficient_gap(isolated_project_env: Path) -> None:
    """Test that spacer STL is created when gaps exceed 4mm threshold."""
    from gridfinity_invoke.generators import generate_drawer_fit

    tmpdir = isolated_project_env
    baseplate_path = tmpdir / "baseplate.stl"
    spacer_path = tmpdir / "spacers.stl"

    # 200mm drawer -> 4 units (168mm) -> 32mm gap total -> 16mm per side (> 4mm)
    result = generate_drawer_fit(200.0, 200.0, baseplate_path, spacer_path)

    # Verify spacer file was created due to large gap
    assert result.spacer_path is not None
    assert result.spacer_path.exists()
    assert result.spacer_path.stat().st_size > 0


def test_no_spacer_for_small_gap(isolated_project_env: Path) -> None:
    """Test that no spacer STL is created when gaps are below 4mm threshold."""
    from gridfinity_invoke.generators import generate_drawer_fit

    tmpdir = isolated_project_env
    baseplate_path = tmpdir / "baseplate.stl"
    spacer_path = tmpdir / "spacers.stl"

    # 88mm drawer -> 2 units (84mm) -> 4mm gap total -> 2mm per side (< 4mm)
    result = generate_drawer_fit(88.0, 88.0, baseplate_path, spacer_path)

    # Verify no spacer file was created (gap too small)
    assert result.spacer_path is None
    assert not spacer_path.exists()
