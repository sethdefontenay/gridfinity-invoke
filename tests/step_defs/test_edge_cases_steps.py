"""Step definitions for edge cases feature tests.

Re-uses step definitions from conftest.py and other test modules.
"""

from unittest.mock import patch

from pytest_bdd import parsers, scenarios, then, when

from gridfinity_invoke import config, projects

scenarios("../features/edge_cases.feature")


# Step definitions that match the edge cases feature file patterns
# These are already defined in conftest.py and other test files
# but pytest-bdd requires them to be imported or redefined


@when(
    parsers.parse("I generate a baseplate with length {length:d} and width {width:d}")
)
def generate_baseplate_custom(scenario_context, length, width, capsys):
    """Generate a baseplate with custom dimensions."""
    from invoke import MockContext
    from invoke_collections.gf import baseplate

    tmpdir = scenario_context["tmpdir"]
    projects_dir = scenario_context["projects_dir"]
    active_file = scenario_context["active_file"]
    config_file = scenario_context["config_file"]

    ctx = MockContext()

    # Check if we have an active project
    project_name = scenario_context.get("project_name")

    with patch.object(projects, "PROJECTS_DIR", projects_dir):
        with patch.object(projects, "ACTIVE_FILE", active_file):
            with patch.object(config, "CONFIG_FILE", config_file):
                try:
                    if project_name:
                        with patch(
                            "invoke_collections.gf.prompt_with_default",
                            return_value=f"baseplate-{length}x{width}",
                        ):
                            baseplate(ctx, length=length, width=width)
                    else:
                        output_path = str(tmpdir / "baseplate.stl")
                        baseplate(ctx, length=length, width=width, output=output_path)
                    scenario_context["exit_code"] = 0
                except SystemExit as e:
                    scenario_context["exit_code"] = e.code

    captured = capsys.readouterr()
    scenario_context["output"] = captured.out + captured.err


@when(
    parsers.parse(
        "I generate a bin with length {length:d}, width {width:d}, "
        "and height {height:d}"
    )
)
def generate_bin_custom(scenario_context, length, width, height, capsys):
    """Generate a bin with custom dimensions."""
    from invoke import MockContext
    from invoke_collections.gf import bin

    tmpdir = scenario_context["tmpdir"]
    projects_dir = scenario_context["projects_dir"]
    active_file = scenario_context["active_file"]
    config_file = scenario_context["config_file"]

    ctx = MockContext()

    # Check if we have an active project
    project_name = scenario_context.get("project_name")

    with patch.object(projects, "PROJECTS_DIR", projects_dir):
        with patch.object(projects, "ACTIVE_FILE", active_file):
            with patch.object(config, "CONFIG_FILE", config_file):
                try:
                    if project_name:
                        with patch(
                            "invoke_collections.gf.prompt_with_default",
                            return_value=f"bin-{length}x{width}x{height}",
                        ):
                            bin(ctx, length=length, width=width, height=height)
                    else:
                        output_path = str(tmpdir / "bin.stl")
                        bin(
                            ctx,
                            length=length,
                            width=width,
                            height=height,
                            output=output_path,
                        )
                    scenario_context["exit_code"] = 0
                except SystemExit as e:
                    scenario_context["exit_code"] = e.code

    captured = capsys.readouterr()
    scenario_context["output"] = captured.out + captured.err


@when(parsers.parse("I generate a drawer-fit with width {width:d} and depth {depth:d}"))
def generate_drawer_fit(scenario_context, width, depth, capsys):
    """Generate a drawer-fit solution with given dimensions."""
    from invoke import MockContext
    from invoke_collections.gf import drawer_fit

    tmpdir = scenario_context["tmpdir"]
    projects_dir = scenario_context["projects_dir"]
    active_file = scenario_context["active_file"]
    config_file = scenario_context["config_file"]

    ctx = MockContext()
    output_path = str(tmpdir / "drawer-fit")

    with patch.object(projects, "PROJECTS_DIR", projects_dir):
        with patch.object(projects, "ACTIVE_FILE", active_file):
            with patch.object(config, "CONFIG_FILE", config_file):
                try:
                    drawer_fit(
                        ctx, width=float(width), depth=float(depth), output=output_path
                    )
                    scenario_context["exit_code"] = 0
                except SystemExit as e:
                    scenario_context["exit_code"] = e.code

    captured = capsys.readouterr()
    scenario_context["output"] = captured.out + captured.err


@when("I run gf.config with --show flag")
def run_config_show(scenario_context, capsys):
    """Run gf.config --show."""
    from invoke import MockContext
    from invoke_collections.gf import config as gf_config

    projects_dir = scenario_context["projects_dir"]
    active_file = scenario_context["active_file"]
    config_file = scenario_context["config_file"]

    ctx = MockContext()

    with patch.object(projects, "PROJECTS_DIR", projects_dir):
        with patch.object(projects, "ACTIVE_FILE", active_file):
            with patch.object(config, "CONFIG_FILE", config_file):
                try:
                    gf_config(ctx, init=False, show=True)
                    scenario_context["exit_code"] = 0
                except SystemExit as e:
                    scenario_context["exit_code"] = e.code

    captured = capsys.readouterr()
    scenario_context["output"] = captured.out + captured.err


@then("the drawer-fit baseplate STL file should exist")
def drawer_fit_stl_exists(scenario_context):
    """Verify the drawer-fit baseplate STL file was created."""
    tmpdir = scenario_context["tmpdir"]
    stl_files = list(tmpdir.glob("**/*.stl"))
    assert any("baseplate" in f.name.lower() for f in stl_files), (
        f"No drawer-fit baseplate STL found in {tmpdir}. Files: {stl_files}"
    )
