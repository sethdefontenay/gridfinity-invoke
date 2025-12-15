"""Step definitions for baseplate feature tests."""

from unittest.mock import patch

from pytest_bdd import parsers, scenarios, when

from gridfinity_invoke import config, projects

scenarios("../features/baseplate.feature")


@when("I generate a baseplate with default dimensions")
def generate_baseplate_default(scenario_context):
    """Generate a baseplate with default 4x4 dimensions."""
    from invoke import MockContext
    from invoke_collections.gf import baseplate

    tmpdir = scenario_context["tmpdir"]
    projects_dir = scenario_context["projects_dir"]
    active_file = scenario_context["active_file"]
    config_file = scenario_context["config_file"]

    ctx = MockContext()
    output_path = str(tmpdir / "baseplate.stl")

    with patch.object(projects, "PROJECTS_DIR", projects_dir):
        with patch.object(projects, "ACTIVE_FILE", active_file):
            with patch.object(config, "CONFIG_FILE", config_file):
                try:
                    baseplate(ctx, length=4, width=4, output=output_path)
                    scenario_context["exit_code"] = 0
                except SystemExit as e:
                    scenario_context["exit_code"] = e.code


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
                        # Mock the prompt to accept default name
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
