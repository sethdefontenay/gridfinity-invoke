"""Invoke tasks for gridfinity-invoke project."""

import json
import sys

from colorama import Fore, Style, init
from invoke import task
from invoke.context import Context

# Initialize colorama for cross-platform colored output
init(autoreset=True)


def print_header(message: str) -> None:
    """Print a formatted header message."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}>>> {message}{Style.RESET_ALL}")


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"{Fore.RED}{message}{Style.RESET_ALL}")


def prompt_with_default(prompt: str, default: str) -> str:
    """Prompt user for input with a default value.

    Displays prompt in format "Name [default]: " and returns user input
    or the default value if the user presses Enter without typing anything.

    Args:
        prompt: The prompt text to display (e.g., "Name").
        default: The default value to use if user enters nothing.

    Returns:
        User input or default if empty.
    """
    user_input = input(f"{prompt} [{default}]: ").strip()
    return user_input if user_input else default


def format_task_help(name: str, docstring: str | None) -> str:
    """Format a task's JSON docstring into pretty help text."""
    lines = []
    lines.append(f"{Fore.CYAN}{Style.BRIGHT}{name}{Style.RESET_ALL}")

    if not docstring:
        lines.append(f"  {Fore.YELLOW}No description available{Style.RESET_ALL}")
        return "\n".join(lines)

    # Try to parse as JSON
    try:
        doc = json.loads(docstring.strip())
    except json.JSONDecodeError:
        # Not JSON, just show raw docstring
        lines.append(f"  {docstring.strip()}")
        return "\n".join(lines)

    # Description
    if desc := doc.get("desc"):
        lines.append(f"  {desc}")

    # Parameters
    if params := doc.get("params"):
        lines.append(f"\n  {Fore.GREEN}Parameters:{Style.RESET_ALL}")
        for param in params:
            param_name = param.get("name", "?")
            param_type = param.get("type", "")
            param_desc = param.get("desc", "")
            param_example = param.get("example", "")

            type_str = f" ({param_type})" if param_type else ""
            lines.append(f"    --{param_name}{type_str}")
            if param_desc:
                lines.append(f"        {param_desc}")
            if param_example:
                lines.append(
                    f"        {Fore.YELLOW}Example: {param_example}{Style.RESET_ALL}"
                )  # noqa: E501

    return "\n".join(lines)


@task
def pp(ctx: Context) -> None:
    """{"desc": "Pretty print all available commands with formatted help", "params": [], "returns": {}}"""  # noqa: E501
    import tasks as task_module

    print_header("Available Commands")
    print()

    # Get all task functions from the module
    task_funcs = []
    for name in dir(task_module):
        obj = getattr(task_module, name)
        # Check if it's a task (has __wrapped__ from @task decorator)
        if callable(obj) and hasattr(obj, "__wrapped__"):
            # Get the display name (use task name if set, otherwise function name)
            display_name = name.replace("_", "-")
            task_funcs.append((display_name, obj.__doc__))

    # Sort by name and print
    for name, docstring in sorted(task_funcs):
        print(format_task_help(name, docstring))
        print()


@task
def lint(ctx: Context) -> None:
    """
    {"desc": "Run ruff linter on source and test files", "params": [], "returns": {}}
    """
    print_header("Running ruff linter...")
    result = ctx.run("ruff check src/ tests/", warn=True)
    if result is None or result.failed:
        print_error("Linting failed!")
        sys.exit(1)
    print_success("Linting passed!")


@task
def format(ctx: Context, check: bool = False) -> None:
    """{"desc": "Run ruff formatter on source and test files", "params": [{"name": "check", "type": "bool", "desc": "Check formatting without modifying files (CI mode)", "example": "true"}], "returns": {}}"""  # noqa: E501
    if check:
        print_header("Checking code formatting...")
        cmd = "ruff format --check src/ tests/"
    else:
        print_header("Formatting code...")
        cmd = "ruff format src/ tests/"

    result = ctx.run(cmd, warn=True)
    if result is None or result.failed:
        if check:
            print_error("Formatting check failed! Run 'invoke format' to fix.")
        else:
            print_error("Formatting failed!")
        sys.exit(1)

    if check:
        print_success("Code is properly formatted!")
    else:
        print_success("Formatting complete!")


@task
def test(ctx: Context, verbose: bool = False) -> None:
    """{"desc": "Run pytest with coverage reporting", "params": [{"name": "verbose", "type": "bool", "desc": "Enable verbose output", "example": "true"}], "returns": {}}"""  # noqa: E501
    print_header("Running tests with coverage...")
    # Use sys.executable to ensure we use the same Python as invoke
    cmd = f"{sys.executable} -m pytest"
    if verbose:
        cmd += " -v"

    result = ctx.run(cmd, warn=True)
    if result is None or result.failed:
        print_error("Tests failed!")
        sys.exit(1)
    print_success("All tests passed!")


@task
def check(ctx: Context) -> None:
    """{"desc": "Run lint and test in sequence, failing fast on lint errors", "params": [], "returns": {}}"""  # noqa: E501
    print_header("Running full quality check (lint + test)...")

    # Run lint first - fail fast if lint fails
    print_header("Step 1/2: Running linter...")
    lint_result = ctx.run("ruff check src/ tests/", warn=True)
    if lint_result is None or lint_result.failed:
        print_error("Lint failed! Skipping tests.")
        sys.exit(1)
    print_success("Lint passed!")

    # Run tests only if lint passes
    print_header("Step 2/2: Running tests...")
    test_result = ctx.run(f"{sys.executable} -m pytest", warn=True)
    if test_result is None or test_result.failed:
        print_error("Tests failed!")
        sys.exit(1)

    print_success("All quality checks passed!")


@task
def bin(
    ctx: Context,
    length: int = 2,
    width: int = 2,
    height: int = 3,
    output: str = "output/bin.stl",
) -> None:
    """{"desc": "Generate a Gridfinity bin and export to STL", "params": [{"name": "length", "type": "int", "desc": "Length in gridfinity units (1 unit = 42mm)", "example": "2"}, {"name": "width", "type": "int", "desc": "Width in gridfinity units", "example": "2"}, {"name": "height", "type": "int", "desc": "Height in gridfinity units (1 unit = 7mm)", "example": "3"}, {"name": "output", "type": "string", "desc": "Output path for the STL file", "example": "output/bin.stl"}], "returns": {}}"""  # noqa: E501
    from gridfinity_invoke.generators import generate_bin
    from gridfinity_invoke.projects import (
        add_component_to_config,
        get_active_project,
        get_project_path,
    )

    print_header(f"Generating {length}x{width}x{height} Gridfinity bin...")

    if length < 1 or width < 1 or height < 1:
        print_error("All dimensions must be positive integers >= 1")
        sys.exit(1)

    # Check for active project
    active_project = get_active_project()

    if active_project:
        # Project-aware behavior: prompt for name and save to project
        default_name = f"bin-{length}x{width}x{height}"
        component_name = prompt_with_default("Name", default_name)

        # Save to project directory
        project_path = get_project_path(active_project)
        output_path = project_path / f"{component_name}.stl"

        try:
            result_path = generate_bin(length, width, height, output_path)
            print_success(f"Generated: {result_path}")

            # Add component to config
            component = {
                "name": component_name,
                "type": "bin",
                "length": length,
                "width": width,
                "height": height,
            }
            add_component_to_config(active_project, component)
            print_success(f"Added to project: {active_project}")
        except Exception as e:
            print_error(f"Generation failed: {e}")
            sys.exit(1)
    else:
        # Default behavior: save to output directory
        try:
            result_path = generate_bin(length, width, height, output)
            print_success(f"Generated: {result_path}")
        except Exception as e:
            print_error(f"Generation failed: {e}")
            sys.exit(1)


@task
def baseplate(
    ctx: Context,
    length: int = 4,
    width: int = 4,
    output: str = "output/baseplate.stl",
) -> None:
    """{"desc": "Generate a Gridfinity baseplate and export to STL", "params": [{"name": "length", "type": "int", "desc": "Length in gridfinity units (1 unit = 42mm)", "example": "4"}, {"name": "width", "type": "int", "desc": "Width in gridfinity units", "example": "4"}, {"name": "output", "type": "string", "desc": "Output path for the STL file", "example": "output/baseplate.stl"}], "returns": {}}"""  # noqa: E501
    from gridfinity_invoke.generators import generate_baseplate
    from gridfinity_invoke.projects import (
        add_component_to_config,
        get_active_project,
        get_project_path,
    )

    print_header(f"Generating {length}x{width} Gridfinity baseplate...")

    if length < 1 or width < 1:
        print_error("All dimensions must be positive integers >= 1")
        sys.exit(1)

    # Check for active project
    active_project = get_active_project()

    if active_project:
        # Project-aware behavior: prompt for name and save to project
        default_name = f"baseplate-{length}x{width}"
        component_name = prompt_with_default("Name", default_name)

        # Save to project directory
        project_path = get_project_path(active_project)
        output_path = project_path / f"{component_name}.stl"

        try:
            result_path = generate_baseplate(length, width, output_path)
            print_success(f"Generated: {result_path}")

            # Add component to config
            component = {
                "name": component_name,
                "type": "baseplate",
                "length": length,
                "width": width,
            }
            add_component_to_config(active_project, component)
            print_success(f"Added to project: {active_project}")
        except Exception as e:
            print_error(f"Generation failed: {e}")
            sys.exit(1)
    else:
        # Default behavior: save to output directory
        try:
            result_path = generate_baseplate(length, width, output)
            print_success(f"Generated: {result_path}")
        except Exception as e:
            print_error(f"Generation failed: {e}")
            sys.exit(1)


@task(name="new-project")
def new_project(ctx: Context, name: str) -> None:
    """{"desc": "Create a new Gridfinity project", "params": [{"name": "name", "type": "string", "desc": "Project name", "example": "my-project"}], "returns": {}}"""  # noqa: E501
    from gridfinity_invoke.projects import (
        get_project_path,
        save_project_config,
        set_active_project,
    )

    print_header(f"Creating new project: {name}")

    project_path = get_project_path(name)

    # Check if project already exists
    if project_path.exists():
        print_error(f"Project '{name}' already exists!")
        sys.exit(1)

    # Create initial config
    config = {"name": name, "components": []}
    save_project_config(name, config)

    # Set as active project
    set_active_project(name)

    print_success(f"Created project: {name}")
    print_success(f"Project directory: {project_path}")
    print_success(f"Active project set to: {name}")


@task
def load(ctx: Context, project: str) -> None:
    """{"desc": "Load a Gridfinity project and regenerate all STL files", "params": [{"name": "project", "type": "string", "desc": "Project name to load", "example": "my-project"}], "returns": {}}"""  # noqa: E501
    from gridfinity_invoke.generators import generate_baseplate, generate_bin
    from gridfinity_invoke.projects import (
        get_project_path,
        load_project_config,
        set_active_project,
    )

    print_header(f"Loading project: {project}")

    project_path = get_project_path(project)

    # Check if project exists
    if not project_path.exists():
        print_error(f"Project '{project}' does not exist!")
        sys.exit(1)

    # Load config
    try:
        config = load_project_config(project)
    except FileNotFoundError:
        print_error(f"Project config not found for '{project}'!")
        sys.exit(1)

    # Regenerate all STL files
    components = config.get("components", [])
    print_header(f"Regenerating {len(components)} component(s)...")

    for component in components:
        component_name = component["name"]
        component_type = component["type"]
        output_path = project_path / f"{component_name}.stl"

        if component_type == "bin":
            length = component["length"]
            width = component["width"]
            height = component["height"]
            print(f"  Generating bin: {component_name} ({length}x{width}x{height})")
            generate_bin(length, width, height, output_path)
        elif component_type == "baseplate":
            length = component["length"]
            width = component["width"]
            print(f"  Generating baseplate: {component_name} ({length}x{width})")
            generate_baseplate(length, width, output_path)

    # Set as active project
    set_active_project(project)

    print_success(f"Loaded project: {project}")
    print_success(f"Active project set to: {project}")


@task(name="list-projects")
def list_projects(ctx: Context) -> None:
    """{"desc": "List all Gridfinity projects", "params": [], "returns": {}}"""
    from gridfinity_invoke.projects import PROJECTS_DIR, get_active_project

    print_header("Gridfinity Projects")

    # Check if projects directory exists
    if not PROJECTS_DIR.exists():
        print("No projects found")
        return

    # List all project directories
    projects = [d for d in PROJECTS_DIR.iterdir() if d.is_dir()]

    if not projects:
        print("No projects found")
        return

    # Get active project
    active_project = get_active_project()

    # Print projects with active indicator
    for project in sorted(projects, key=lambda p: p.name):
        if project.name == active_project:
            print(f"  * {project.name} (active)")
        else:
            print(f"    {project.name}")
