"""Step definitions for project management feature tests."""

from unittest.mock import patch

from pytest_bdd import given, parsers, scenarios, then, when

from gridfinity_invoke import config, projects

scenarios("../features/new_project.feature")
scenarios("../features/load.feature")
scenarios("../features/list_projects.feature")


# Given steps for project setup


@given(parsers.parse('an existing project named "{project_name}" with components'))
def existing_project_with_components(scenario_context, project_name):
    """Set up an existing project with some components."""
    import json
    import tempfile
    from pathlib import Path

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

    # Create the project with components
    with patch.object(projects, "PROJECTS_DIR", projects_dir):
        with patch.object(projects, "ACTIVE_FILE", active_file):
            with patch.object(config, "CONFIG_FILE", config_file):
                from invoke import MockContext
                from invoke_collections.gf import new_project

                ctx = MockContext()
                new_project(ctx, name=project_name)

                # Add components to config
                project_config = {
                    "name": project_name,
                    "components": [
                        {
                            "name": "test-bin",
                            "type": "bin",
                            "length": 2,
                            "width": 2,
                            "height": 3,
                        },
                    ],
                }
                projects.save_project_config(project_name, project_config)


@given(
    parsers.parse('an existing project named "{project_name}" with mixed components')
)
def existing_project_with_mixed_components(scenario_context, project_name):
    """Set up an existing project with both bins and baseplates."""
    import json
    import tempfile
    from pathlib import Path

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

    # Create the project with mixed components
    with patch.object(projects, "PROJECTS_DIR", projects_dir):
        with patch.object(projects, "ACTIVE_FILE", active_file):
            with patch.object(config, "CONFIG_FILE", config_file):
                from invoke import MockContext
                from invoke_collections.gf import new_project

                ctx = MockContext()
                new_project(ctx, name=project_name)

                # Add mixed components to config
                project_config = {
                    "name": project_name,
                    "components": [
                        {
                            "name": "test-bin",
                            "type": "bin",
                            "length": 1,
                            "width": 1,
                            "height": 1,
                        },
                        {
                            "name": "test-baseplate",
                            "type": "baseplate",
                            "length": 2,
                            "width": 2,
                        },
                    ],
                }
                projects.save_project_config(project_name, project_config)


@given("multiple projects exist")
def multiple_projects_exist(scenario_context):
    """Set up state with multiple existing projects."""
    import json
    import tempfile
    from pathlib import Path

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

    # Create multiple projects
    with patch.object(projects, "PROJECTS_DIR", projects_dir):
        with patch.object(projects, "ACTIVE_FILE", active_file):
            with patch.object(config, "CONFIG_FILE", config_file):
                from invoke import MockContext
                from invoke_collections.gf import new_project

                ctx = MockContext()
                new_project(ctx, name="project-a")
                new_project(ctx, name="project-b")

    scenario_context["project_names"] = ["project-a", "project-b"]


# When steps


@when(parsers.parse('I create a new project named "{project_name}"'))
def create_new_project(scenario_context, project_name, capsys):
    """Create a new project."""
    from invoke import MockContext
    from invoke_collections.gf import new_project

    projects_dir = scenario_context["projects_dir"]
    active_file = scenario_context["active_file"]
    config_file = scenario_context["config_file"]

    ctx = MockContext()

    with patch.object(projects, "PROJECTS_DIR", projects_dir):
        with patch.object(projects, "ACTIVE_FILE", active_file):
            with patch.object(config, "CONFIG_FILE", config_file):
                try:
                    new_project(ctx, name=project_name)
                    scenario_context["exit_code"] = 0
                except SystemExit as e:
                    scenario_context["exit_code"] = e.code

    captured = capsys.readouterr()
    scenario_context["output"] = captured.out + captured.err
    scenario_context["project_name"] = project_name


@when(parsers.parse('I try to create another project named "{project_name}"'))
def try_create_duplicate_project(scenario_context, project_name, capsys):
    """Try to create a duplicate project (expected to fail)."""
    from invoke import MockContext
    from invoke_collections.gf import new_project

    projects_dir = scenario_context["projects_dir"]
    active_file = scenario_context["active_file"]
    config_file = scenario_context["config_file"]

    ctx = MockContext()

    with patch.object(projects, "PROJECTS_DIR", projects_dir):
        with patch.object(projects, "ACTIVE_FILE", active_file):
            with patch.object(config, "CONFIG_FILE", config_file):
                try:
                    new_project(ctx, name=project_name)
                    scenario_context["exit_code"] = 0
                except SystemExit as e:
                    scenario_context["exit_code"] = e.code

    captured = capsys.readouterr()
    scenario_context["output"] = captured.out + captured.err


@when(parsers.parse('I load the project "{project_name}"'))
def load_project(scenario_context, project_name, capsys):
    """Load an existing project."""
    from invoke import MockContext
    from invoke_collections.gf import load

    projects_dir = scenario_context["projects_dir"]
    active_file = scenario_context["active_file"]
    config_file = scenario_context["config_file"]

    ctx = MockContext()

    with patch.object(projects, "PROJECTS_DIR", projects_dir):
        with patch.object(projects, "ACTIVE_FILE", active_file):
            with patch.object(config, "CONFIG_FILE", config_file):
                try:
                    load(ctx, project=project_name)
                    scenario_context["exit_code"] = 0
                except SystemExit as e:
                    scenario_context["exit_code"] = e.code

    captured = capsys.readouterr()
    scenario_context["output"] = captured.out + captured.err


@when(parsers.parse('I try to load the project "{project_name}"'))
def try_load_nonexistent_project(scenario_context, project_name, capsys):
    """Try to load a non-existent project (expected to fail)."""
    from invoke import MockContext
    from invoke_collections.gf import load

    projects_dir = scenario_context["projects_dir"]
    active_file = scenario_context["active_file"]
    config_file = scenario_context["config_file"]

    ctx = MockContext()

    with patch.object(projects, "PROJECTS_DIR", projects_dir):
        with patch.object(projects, "ACTIVE_FILE", active_file):
            with patch.object(config, "CONFIG_FILE", config_file):
                try:
                    load(ctx, project=project_name)
                    scenario_context["exit_code"] = 0
                except SystemExit as e:
                    scenario_context["exit_code"] = e.code

    captured = capsys.readouterr()
    scenario_context["output"] = captured.out + captured.err


@when("I list all projects")
def list_all_projects(scenario_context, capsys):
    """List all projects."""
    from invoke import MockContext
    from invoke_collections.gf import list_projects

    projects_dir = scenario_context["projects_dir"]
    active_file = scenario_context["active_file"]
    config_file = scenario_context["config_file"]

    ctx = MockContext()

    with patch.object(projects, "PROJECTS_DIR", projects_dir):
        with patch.object(projects, "ACTIVE_FILE", active_file):
            with patch.object(config, "CONFIG_FILE", config_file):
                try:
                    list_projects(ctx)
                    scenario_context["exit_code"] = 0
                except SystemExit as e:
                    scenario_context["exit_code"] = e.code

    captured = capsys.readouterr()
    scenario_context["output"] = captured.out + captured.err


# Then steps


@then("the project directory should exist")
def project_directory_exists(scenario_context):
    """Verify the project directory was created."""
    projects_dir = scenario_context["projects_dir"]
    project_name = scenario_context["project_name"]
    project_dir = projects_dir / project_name
    assert project_dir.exists(), f"Project directory not found: {project_dir}"


@then("the project config.json should exist")
def project_config_exists(scenario_context):
    """Verify the project config.json was created."""
    projects_dir = scenario_context["projects_dir"]
    project_name = scenario_context["project_name"]
    config_path = projects_dir / project_name / "config.json"
    assert config_path.exists(), f"Config file not found: {config_path}"


@then("the project should be set as active")
def project_is_active(scenario_context):
    """Verify the project is set as active."""
    projects_dir = scenario_context["projects_dir"]
    active_file = scenario_context["active_file"]
    project_name = scenario_context["project_name"]

    with patch.object(projects, "PROJECTS_DIR", projects_dir):
        with patch.object(projects, "ACTIVE_FILE", active_file):
            active_project = projects.get_active_project()
            assert active_project == project_name, (
                f"Expected active project '{project_name}', got '{active_project}'"
            )


@then("the STL files should be regenerated")
def stl_files_regenerated(scenario_context):
    """Verify STL files were regenerated."""
    projects_dir = scenario_context["projects_dir"]
    project_name = scenario_context["project_name"]
    project_dir = projects_dir / project_name
    stl_files = list(project_dir.glob("*.stl"))
    assert len(stl_files) > 0, f"No STL files found in {project_dir}"


@then("both bin and baseplate STL files should exist")
def both_stl_types_exist(scenario_context):
    """Verify both bin and baseplate STL files exist."""
    projects_dir = scenario_context["projects_dir"]
    project_name = scenario_context["project_name"]
    project_dir = projects_dir / project_name
    stl_files = list(project_dir.glob("*.stl"))

    has_bin = any("bin" in f.name.lower() for f in stl_files)
    has_baseplate = any("baseplate" in f.name.lower() for f in stl_files)

    assert has_bin, f"No bin STL found in {project_dir}. Files: {stl_files}"
    assert has_baseplate, f"No baseplate STL found in {project_dir}. Files: {stl_files}"


@then("the output should contain project names")
def output_contains_project_names(scenario_context):
    """Verify output contains project names."""
    output = scenario_context.get("output", "")
    project_names = scenario_context.get("project_names", [])
    for name in project_names:
        assert name in output, f"Expected '{name}' in output: {output}"


@then("the active project should be marked")
def active_project_is_marked(scenario_context):
    """Verify the active project is marked in the output."""
    output = scenario_context.get("output", "")
    # The active project should have an asterisk or "(active)" marker
    assert "*" in output or "active" in output.lower(), (
        f"No active marker found in output: {output}"
    )
