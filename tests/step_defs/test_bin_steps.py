"""Step definitions for bin feature tests."""

from unittest.mock import patch

from pytest_bdd import parsers, scenarios, when

from gridfinity_invoke import config, projects

scenarios("../features/bin.feature")


@when("I generate a bin with default dimensions")
def generate_bin_default(scenario_context):
    """Generate a bin with default 2x2x3 dimensions."""
    from invoke import MockContext
    from invoke_collections.gf import bin

    tmpdir = scenario_context["tmpdir"]
    projects_dir = scenario_context["projects_dir"]
    active_file = scenario_context["active_file"]
    config_file = scenario_context["config_file"]

    ctx = MockContext()
    output_path = str(tmpdir / "bin.stl")

    with patch.object(projects, "PROJECTS_DIR", projects_dir):
        with patch.object(projects, "ACTIVE_FILE", active_file):
            with patch.object(config, "CONFIG_FILE", config_file):
                try:
                    bin(ctx, length=2, width=2, height=3, output=output_path)
                    scenario_context["exit_code"] = 0
                except SystemExit as e:
                    scenario_context["exit_code"] = e.code


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
                        # Mock the prompt to accept default name
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
