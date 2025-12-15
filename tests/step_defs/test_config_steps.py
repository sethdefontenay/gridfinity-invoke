"""Step definitions for config feature tests."""

from unittest.mock import patch

from pytest_bdd import scenarios, when

from gridfinity_invoke import config, projects

scenarios("../features/config.feature")


@when("I run gf.config with --init flag providing dimensions")
def run_config_init(scenario_context, capsys):
    """Run gf.config --init with mocked user input."""
    from invoke import MockContext
    from invoke_collections.gf import config as gf_config

    projects_dir = scenario_context["projects_dir"]
    active_file = scenario_context["active_file"]
    config_file = scenario_context["config_file"]

    ctx = MockContext()

    with patch.object(projects, "PROJECTS_DIR", projects_dir):
        with patch.object(projects, "ACTIVE_FILE", active_file):
            with patch.object(config, "CONFIG_FILE", config_file):
                # Mock prompts for bed dimensions
                with patch(
                    "invoke_collections.gf.prompt_with_default",
                    side_effect=["225", "225"],
                ):
                    try:
                        gf_config(ctx, init=True, show=False)
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


@when("I run gf.config without flags")
def run_config_no_flags(scenario_context, capsys):
    """Run gf.config without any flags."""
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
                    gf_config(ctx, init=False, show=False)
                    scenario_context["exit_code"] = 0
                except SystemExit as e:
                    scenario_context["exit_code"] = e.code

    captured = capsys.readouterr()
    scenario_context["output"] = captured.out + captured.err
