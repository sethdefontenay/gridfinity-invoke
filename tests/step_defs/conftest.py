"""Shared fixtures and step definitions for BDD tests."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from pytest_bdd import given, parsers, then

from gridfinity_invoke import config, projects

# Mock the cqgridfinity module before it's imported by generators
_mock_cqgridfinity = MagicMock()


class MockGridfinityBaseplate:
    def __init__(self, *args, **kwargs):
        pass

    def render(self):
        mock_obj = MagicMock()
        mock_obj.val.return_value.exportStl = lambda p: Path(p).write_text("mock")
        return mock_obj


class MockGridfinityBox:
    def __init__(self, *args, **kwargs):
        pass

    def render(self):
        mock_obj = MagicMock()
        mock_obj.val.return_value.exportStl = lambda p: Path(p).write_text("mock")
        return mock_obj


class MockGridfinityDrawerSpacer:
    def __init__(self, *args, **kwargs):
        pass

    def render_half_set(self):
        mock_obj = MagicMock()
        mock_obj.val.return_value.exportStl = lambda p: Path(p).write_text("mock")
        return mock_obj


_mock_cqgridfinity.GridfinityBaseplate = MockGridfinityBaseplate
_mock_cqgridfinity.GridfinityBox = MockGridfinityBox
_mock_cqgridfinity.GridfinityDrawerSpacer = MockGridfinityDrawerSpacer


@pytest.fixture(autouse=True, scope="session")
def mock_cqgridfinity():
    """Mock cqgridfinity module at session scope before any imports."""
    sys.modules["cqgridfinity"] = _mock_cqgridfinity
    yield
    # Clean up if needed (usually not necessary in tests)


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for output files with isolated project state."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        active_file = tmpdir_path / ".gridfinity-active"
        projects_dir = tmpdir_path / "projects"
        config_file = tmpdir_path / ".gf-config"
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


@pytest.fixture
def temp_project_dir():
    """Create a temporary directory for project tests with isolated state."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        active_file = tmpdir_path / ".gridfinity-active"
        projects_dir = tmpdir_path / "projects"
        config_file = tmpdir_path / ".gf-config"
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


@pytest.fixture
def cli_runner():
    """Fixture for running CLI commands via subprocess."""

    def run_command(
        args: list[str], cwd: Path | None = None
    ) -> subprocess.CompletedProcess[str]:
        """Run an invoke command and return the result."""
        cmd = [sys.executable, "-m", "invoke"] + args
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd or Path(__file__).parent.parent.parent,
        )

    return run_command


@pytest.fixture
def isolated_config():
    """Fixture for isolated config file testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        config_file = tmpdir_path / ".gf-config"
        with patch.object(config, "CONFIG_FILE", config_file):
            yield config_file


@pytest.fixture
def scenario_context() -> dict[str, Any]:
    """Shared context for passing data between Given/When/Then steps."""
    return {}


# Common Given steps


@given("a clean output directory")
def clean_output_directory(scenario_context):
    """Set up a clean temporary output directory with isolated state."""
    tmpdir = tempfile.mkdtemp()
    tmpdir_path = Path(tmpdir)
    active_file = tmpdir_path / ".gridfinity-active"
    projects_dir = tmpdir_path / "projects"
    config_file = tmpdir_path / ".gf-config"
    config_file.write_text(
        json.dumps(
            {
                "print_bed_width_mm": 225,
                "print_bed_depth_mm": 225,
            },
            indent=2,
        )
    )
    scenario_context["tmpdir"] = tmpdir_path
    scenario_context["active_file"] = active_file
    scenario_context["projects_dir"] = projects_dir
    scenario_context["config_file"] = config_file
    scenario_context["exit_code"] = 0
    scenario_context["output"] = ""


@given(parsers.parse('an active project named "{project_name}"'))
def active_project(scenario_context, project_name):
    """Set up an active project in a temporary directory."""
    tmpdir = tempfile.mkdtemp()
    tmpdir_path = Path(tmpdir)
    active_file = tmpdir_path / ".gridfinity-active"
    projects_dir = tmpdir_path / "projects"
    config_file = tmpdir_path / ".gf-config"
    config_file.write_text(
        json.dumps(
            {
                "print_bed_width_mm": 225,
                "print_bed_depth_mm": 225,
            },
            indent=2,
        )
    )

    scenario_context["tmpdir"] = tmpdir_path
    scenario_context["active_file"] = active_file
    scenario_context["projects_dir"] = projects_dir
    scenario_context["config_file"] = config_file
    scenario_context["project_name"] = project_name
    scenario_context["exit_code"] = 0
    scenario_context["output"] = ""

    # Create the project
    with patch.object(projects, "PROJECTS_DIR", projects_dir):
        with patch.object(projects, "ACTIVE_FILE", active_file):
            with patch.object(config, "CONFIG_FILE", config_file):
                from invoke import MockContext
                from invoke_collections.gf import new_project

                ctx = MockContext()
                new_project(ctx, name=project_name)


@given("no projects exist")
def no_projects_exist(scenario_context):
    """Set up state with no existing projects."""
    tmpdir = tempfile.mkdtemp()
    tmpdir_path = Path(tmpdir)
    active_file = tmpdir_path / ".gridfinity-active"
    projects_dir = tmpdir_path / "projects"
    config_file = tmpdir_path / ".gf-config"
    config_file.write_text(
        json.dumps(
            {
                "print_bed_width_mm": 225,
                "print_bed_depth_mm": 225,
            },
            indent=2,
        )
    )
    scenario_context["tmpdir"] = tmpdir_path
    scenario_context["active_file"] = active_file
    scenario_context["projects_dir"] = projects_dir
    scenario_context["config_file"] = config_file
    scenario_context["exit_code"] = 0
    scenario_context["output"] = ""


@given("a printer configuration exists")
def printer_config_exists(scenario_context):
    """Set up state with existing printer configuration."""
    tmpdir = tempfile.mkdtemp()
    tmpdir_path = Path(tmpdir)
    active_file = tmpdir_path / ".gridfinity-active"
    projects_dir = tmpdir_path / "projects"
    config_file = tmpdir_path / ".gf-config"
    config_file.write_text(
        json.dumps(
            {
                "print_bed_width_mm": 225,
                "print_bed_depth_mm": 225,
            },
            indent=2,
        )
    )
    scenario_context["tmpdir"] = tmpdir_path
    scenario_context["active_file"] = active_file
    scenario_context["projects_dir"] = projects_dir
    scenario_context["config_file"] = config_file
    scenario_context["exit_code"] = 0
    scenario_context["output"] = ""


@given("no printer configuration exists")
def no_printer_config(scenario_context):
    """Set up state with no printer configuration."""
    tmpdir = tempfile.mkdtemp()
    tmpdir_path = Path(tmpdir)
    active_file = tmpdir_path / ".gridfinity-active"
    projects_dir = tmpdir_path / "projects"
    config_file = tmpdir_path / ".gf-config"
    # Do NOT create config file
    scenario_context["tmpdir"] = tmpdir_path
    scenario_context["active_file"] = active_file
    scenario_context["projects_dir"] = projects_dir
    scenario_context["config_file"] = config_file
    scenario_context["exit_code"] = 0
    scenario_context["output"] = ""


# Common Then steps


@then(parsers.parse("the exit code should be {code:d}"))
def check_exit_code(scenario_context, code):
    """Verify the exit code matches expected value."""
    assert scenario_context.get("exit_code", 0) == code


@then(parsers.parse('the output should contain "{text}"'))
def output_contains(scenario_context, text):
    """Verify the output contains expected text."""
    output = scenario_context.get("output", "")
    assert text.lower() in output.lower(), f"Expected '{text}' in output: {output}"


@then("the baseplate STL file should exist")
def baseplate_stl_exists(scenario_context):
    """Verify the baseplate STL file was created."""
    tmpdir = scenario_context["tmpdir"]
    stl_files = list(tmpdir.glob("**/*.stl"))
    assert any("baseplate" in f.name.lower() for f in stl_files), (
        f"No baseplate STL found in {tmpdir}. Files: {stl_files}"
    )


@then("the bin STL file should exist")
def bin_stl_exists(scenario_context):
    """Verify the bin STL file was created."""
    tmpdir = scenario_context["tmpdir"]
    stl_files = list(tmpdir.glob("**/*.stl"))
    assert any("bin" in f.name.lower() for f in stl_files), (
        f"No bin STL found in {tmpdir}. Files: {stl_files}"
    )


@then("the baseplate STL should exist in the project directory")
def baseplate_stl_in_project(scenario_context):
    """Verify baseplate STL exists in the project directory."""
    projects_dir = scenario_context["projects_dir"]
    project_name = scenario_context["project_name"]
    project_dir = projects_dir / project_name
    stl_files = list(project_dir.glob("*.stl"))
    assert any("baseplate" in f.name.lower() for f in stl_files), (
        f"No baseplate STL found in {project_dir}. Files: {stl_files}"
    )


@then("the bin STL should exist in the project directory")
def bin_stl_in_project(scenario_context):
    """Verify bin STL exists in the project directory."""
    projects_dir = scenario_context["projects_dir"]
    project_name = scenario_context["project_name"]
    project_dir = projects_dir / project_name
    stl_files = list(project_dir.glob("*.stl"))
    assert any("bin" in f.name.lower() for f in stl_files), (
        f"No bin STL found in {project_dir}. Files: {stl_files}"
    )


@then("the project config should contain a baseplate component")
def config_contains_baseplate(scenario_context):
    """Verify project config contains a baseplate component."""
    projects_dir = scenario_context["projects_dir"]
    project_name = scenario_context["project_name"]

    with patch.object(projects, "PROJECTS_DIR", projects_dir):
        config_data = projects.load_project_config(project_name)

    assert any(c["type"] == "baseplate" for c in config_data["components"]), (
        f"No baseplate component in config: {config_data}"
    )
    scenario_context["last_component"] = next(
        c for c in config_data["components"] if c["type"] == "baseplate"
    )


@then("the project config should contain a bin component")
def config_contains_bin(scenario_context):
    """Verify project config contains a bin component."""
    projects_dir = scenario_context["projects_dir"]
    project_name = scenario_context["project_name"]

    with patch.object(projects, "PROJECTS_DIR", projects_dir):
        config_data = projects.load_project_config(project_name)

    assert any(c["type"] == "bin" for c in config_data["components"]), (
        f"No bin component in config: {config_data}"
    )
    scenario_context["last_component"] = next(
        c for c in config_data["components"] if c["type"] == "bin"
    )


@then(parsers.parse("the component should have length {length:d} and width {width:d}"))
def component_has_dimensions_2d(scenario_context, length, width):
    """Verify component has correct 2D dimensions."""
    component = scenario_context["last_component"]
    assert component["length"] == length
    assert component["width"] == width


@then(
    parsers.parse(
        "the component should have length {length:d}, width {width:d}, "
        "and height {height:d}"
    )
)
def component_has_dimensions_3d(scenario_context, length, width, height):
    """Verify component has correct 3D dimensions."""
    component = scenario_context["last_component"]
    assert component["length"] == length
    assert component["width"] == width
    assert component["height"] == height
