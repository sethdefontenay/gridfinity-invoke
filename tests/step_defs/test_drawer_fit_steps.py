"""Step definitions for drawer-fit feature tests."""

from unittest.mock import patch

from pytest_bdd import parsers, scenarios, then, when

from gridfinity_invoke import config, projects

scenarios("../features/drawer_fit.feature")


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


@when(
    parsers.parse(
        "I generate an oversized drawer-fit with width {width:d} and depth {depth:d}"
    )
)
def generate_oversized_drawer_fit(scenario_context, width, depth, capsys):
    """Generate an oversized drawer-fit solution (accepts Y to split prompt)."""
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
                # Mock input() to accept split (answer "y")
                with patch("builtins.input", return_value="y"):
                    try:
                        drawer_fit(
                            ctx,
                            width=float(width),
                            depth=float(depth),
                            output=output_path,
                        )
                        scenario_context["exit_code"] = 0
                    except SystemExit as e:
                        scenario_context["exit_code"] = e.code

    captured = capsys.readouterr()
    scenario_context["output"] = captured.out + captured.err


@when(
    parsers.parse(
        "I generate an oversized drawer-fit with width {width:d} "
        "and depth {depth:d} declining split"
    )
)
def generate_oversized_drawer_fit_no_split(scenario_context, width, depth, capsys):
    """Generate an oversized drawer-fit solution declining split."""
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
                # Mock input() to decline split (answer "n")
                with patch("builtins.input", return_value="n"):
                    try:
                        drawer_fit(
                            ctx,
                            width=float(width),
                            depth=float(depth),
                            output=output_path,
                        )
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
