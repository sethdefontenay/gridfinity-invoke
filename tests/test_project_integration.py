"""Integration tests for project save/load workflow.

These tests verify the complete end-to-end workflow for project management:
- Creating projects
- Adding multiple components (bins and baseplates)
- Loading projects and regenerating STL files
- Config persistence across task invocations
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from invoke import MockContext

from gridfinity_invoke import projects


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


def test_full_workflow_new_project_bins_baseplate_load(
    temp_project_dir: Path,
) -> None:
    """Test full workflow: new-project -> bin -> bin -> baseplate -> load.

    This is the primary end-to-end integration test that verifies:
    1. Creating a new project
    2. Adding multiple bin components
    3. Adding a baseplate component
    4. Loading the project regenerates all STL files
    """
    from invoke_collections.gf import baseplate, bin, load, new_project

    ctx = MockContext()
    project_name = "full-workflow-test"

    # Step 1: Create new project
    new_project(ctx, name=project_name)

    project_dir = temp_project_dir / "projects" / project_name
    assert project_dir.exists()
    assert projects.get_active_project() == project_name

    # Step 2: Add first bin component (2x2x3)
    with patch("invoke_collections.gf.prompt_with_default", return_value="storage-bin"):
        bin(ctx, length=2, width=2, height=3)

    # Step 3: Add second bin component (1x1x4)
    with patch("invoke_collections.gf.prompt_with_default", return_value="small-bin"):
        bin(ctx, length=1, width=1, height=4)

    # Step 4: Add baseplate component (4x4)
    with patch("invoke_collections.gf.prompt_with_default", return_value="main-base"):
        baseplate(ctx, length=4, width=4)

    # Verify all STL files exist
    assert (project_dir / "storage-bin.stl").exists()
    assert (project_dir / "small-bin.stl").exists()
    assert (project_dir / "main-base.stl").exists()

    # Verify config has all 3 components
    config = projects.load_project_config(project_name)
    assert len(config["components"]) == 3

    # Step 5: Delete STL files to simulate fresh load
    (project_dir / "storage-bin.stl").unlink()
    (project_dir / "small-bin.stl").unlink()
    (project_dir / "main-base.stl").unlink()

    # Step 6: Load project to regenerate STLs
    load(ctx, project=project_name)

    # Verify all STL files were regenerated
    assert (project_dir / "storage-bin.stl").exists()
    assert (project_dir / "small-bin.stl").exists()
    assert (project_dir / "main-base.stl").exists()

    # Verify active project is still set correctly
    assert projects.get_active_project() == project_name


def test_load_fails_for_nonexistent_project(temp_project_dir: Path) -> None:
    """Test load fails with error for non-existent project."""
    from invoke_collections.gf import load

    ctx = MockContext()

    # Attempt to load a project that doesn't exist
    with pytest.raises(SystemExit) as exc_info:
        load(ctx, project="nonexistent-project")

    assert exc_info.value.code == 1


def test_config_persistence_across_multiple_operations(
    temp_project_dir: Path,
) -> None:
    """Test config persistence across multiple task invocations.

    Verifies that:
    - Config file is correctly updated after each component addition
    - Component data (type, dimensions) is preserved correctly
    - Multiple components of same type are tracked separately
    """
    from invoke_collections.gf import baseplate, bin, new_project

    ctx = MockContext()
    project_name = "persistence-test"

    # Create project
    new_project(ctx, name=project_name)

    # Add first bin
    with patch("invoke_collections.gf.prompt_with_default", return_value="bin-a"):
        bin(ctx, length=2, width=3, height=4)

    # Verify config after first addition
    config = projects.load_project_config(project_name)
    assert len(config["components"]) == 1
    assert config["components"][0]["name"] == "bin-a"
    assert config["components"][0]["type"] == "bin"
    assert config["components"][0]["length"] == 2
    assert config["components"][0]["width"] == 3
    assert config["components"][0]["height"] == 4

    # Add second bin
    with patch("invoke_collections.gf.prompt_with_default", return_value="bin-b"):
        bin(ctx, length=1, width=1, height=2)

    # Verify config after second addition
    config = projects.load_project_config(project_name)
    assert len(config["components"]) == 2

    # Add baseplate
    with patch("invoke_collections.gf.prompt_with_default", return_value="plate"):
        baseplate(ctx, length=5, width=5)

    # Verify final config
    config = projects.load_project_config(project_name)
    assert len(config["components"]) == 3

    # Verify component types
    types = [c["type"] for c in config["components"]]
    assert types.count("bin") == 2
    assert types.count("baseplate") == 1

    # Verify plate component data
    plate = next(c for c in config["components"] if c["name"] == "plate")
    assert plate["length"] == 5
    assert plate["width"] == 5
    assert "height" not in plate  # baseplates don't have height
