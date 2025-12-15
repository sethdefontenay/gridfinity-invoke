"""Invoke tasks for gridfinity-invoke project."""

import json
import sys
from pathlib import Path

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


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")


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


@task(name="drawer-fit")
def drawer_fit(
    ctx: Context,
    width: float,
    depth: float,
    output: str = "output/drawer-fit",
) -> None:
    """{"desc": "Generate a complete drawer-fit solution from drawer dimensions", "params": [{"name": "width", "type": "float", "desc": "Drawer width (X dimension) in millimeters", "example": "500"}, {"name": "depth", "type": "float", "desc": "Drawer depth (Y dimension) in millimeters", "example": "400"}, {"name": "output", "type": "string", "desc": "Output path prefix for STL files", "example": "output/drawer-fit"}], "returns": {}}"""  # noqa: E501
    from gridfinity_invoke.generators import (
        GRIDFINITY_UNIT_MM,
        MAX_GRIDFINITY_UNITS_X,
        MAX_GRIDFINITY_UNITS_Y,
        MIN_SPACER_GAP_MM,
        PRINT_BED_DEPTH_MM,
        PRINT_BED_WIDTH_MM,
        calculate_baseplate_splits,
        generate_drawer_fit,
        generate_split_baseplates,
    )
    from gridfinity_invoke.projects import (
        add_component_to_config,
        get_active_project,
        get_project_path,
    )

    # Convert string arguments to float (invoke passes CLI args as strings)
    width = float(width)
    depth = float(depth)

    print_header(f"Generating drawer-fit solution for {width}x{depth}mm drawer...")

    # Input validation - positive numbers
    if width <= 0 or depth <= 0:
        print_error("Dimensions must be positive numbers")
        sys.exit(1)

    # Input validation - minimum dimensions
    if width < GRIDFINITY_UNIT_MM:
        print_error(
            f"Width must be at least {GRIDFINITY_UNIT_MM}mm to fit a 1-unit baseplate"
        )
        sys.exit(1)

    if depth < GRIDFINITY_UNIT_MM:
        print_error(
            f"Depth must be at least {GRIDFINITY_UNIT_MM}mm to fit a 1-unit baseplate"
        )
        sys.exit(1)

    # Calculate units for print bed warnings
    units_width = int(width // GRIDFINITY_UNIT_MM)
    units_depth = int(depth // GRIDFINITY_UNIT_MM)

    # Check if splitting is needed
    needs_split = (
        units_width > MAX_GRIDFINITY_UNITS_X or units_depth > MAX_GRIDFINITY_UNITS_Y
    )
    should_split = False

    # Print bed constraint warnings and interactive splitting prompt
    if needs_split:
        actual_width_mm = units_width * GRIDFINITY_UNIT_MM
        actual_depth_mm = units_depth * GRIDFINITY_UNIT_MM
        print_warning(
            f"Warning: Calculated baseplate ({units_width}x{units_depth} units = "
            f"{actual_width_mm}x{actual_depth_mm}mm) exceeds print bed "
            f"({PRINT_BED_WIDTH_MM}x{PRINT_BED_DEPTH_MM}mm)"
        )

        # Calculate and display split suggestion
        splits = calculate_baseplate_splits(units_width, units_depth)
        split_summary = []
        for split_width, split_depth in splits:
            split_summary.append(f"{split_width}x{split_depth}")
        pieces_str = " + ".join(split_summary)
        print_warning(
            f"   Suggestion: Split into {len(splits)} baseplates: {pieces_str} units"
        )

        print()

        # Interactive prompt for splitting (default to Yes)
        response = input("Split into smaller baseplates? [Y/n]: ").strip().lower()
        should_split = response in ("", "y", "yes")

        print()

    # Check for active project
    active_project = get_active_project()

    if active_project:
        # Project-aware behavior: prompt for name and save to project
        default_name = f"drawer-fit-{int(width)}x{int(depth)}mm"
        component_name = prompt_with_default("Name", default_name)

        # Save to project directory
        project_path = get_project_path(active_project)

        try:
            if should_split:
                # Generate split baseplates
                print_header("Generating split baseplates...")
                splits = calculate_baseplate_splits(units_width, units_depth)
                baseplate_paths = generate_split_baseplates(
                    splits, project_path, f"{component_name}-baseplate"
                )

                # Display generated pieces
                for i, (path, (split_w, split_d)) in enumerate(
                    zip(baseplate_paths, splits), start=1
                ):
                    print_success(
                        f"  Generated {path.name} ({split_w}x{split_d} units)"
                    )

                # Generate spacers for full drawer dimensions
                spacer_path = project_path / f"{component_name}-spacers.stl"
                from gridfinity_invoke.generators import DrawerFitResult

                # Calculate gaps for spacer generation
                actual_width_mm = float(units_width * GRIDFINITY_UNIT_MM)
                actual_depth_mm = float(units_depth * GRIDFINITY_UNIT_MM)
                gap_x_mm = width - actual_width_mm
                gap_y_mm = depth - actual_depth_mm
                per_side_gap_x = gap_x_mm / 2
                per_side_gap_y = gap_y_mm / 2

                spacer_result_path = None
                if (
                    per_side_gap_x > MIN_SPACER_GAP_MM
                    or per_side_gap_y > MIN_SPACER_GAP_MM
                ):
                    from cqgridfinity import GridfinityDrawerSpacer

                    spacer_path.parent.mkdir(parents=True, exist_ok=True)
                    spacer = GridfinityDrawerSpacer(dr_width=width, dr_depth=depth)
                    spacer_obj = spacer.render_half_set()
                    if spacer_obj is not None:
                        spacer_obj.val().exportStl(
                            str(spacer_path)
                        )  # pyrefly: ignore[missing-attribute]
                        spacer_result_path = spacer_path

                # Create result object for display
                result = DrawerFitResult(
                    baseplate_path=baseplate_paths[0],  # First piece for compatibility
                    spacer_path=spacer_result_path,
                    units_width=units_width,
                    units_depth=units_depth,
                    actual_width_mm=actual_width_mm,
                    actual_depth_mm=actual_depth_mm,
                    gap_x_mm=gap_x_mm,
                    gap_y_mm=gap_y_mm,
                )

                # Display calculation summary
                _display_drawer_fit_summary(result, width, depth, MIN_SPACER_GAP_MM)

                # Check spacer dimensions against print bed
                if result.spacer_path:
                    if width > PRINT_BED_WIDTH_MM or depth > PRINT_BED_DEPTH_MM:
                        print_warning(
                            f"Warning: Spacer dimensions may exceed print bed "
                            f"({PRINT_BED_WIDTH_MM}x{PRINT_BED_DEPTH_MM}mm)"
                        )
                        print()

                if result.spacer_path:
                    print_success(f"Generated spacers: {result.spacer_path}")
                else:
                    print("No spacers generated (gaps below 4mm threshold)")

                # Add component to config with split_count
                component = {
                    "name": component_name,
                    "type": "drawer-fit",
                    "width_mm": width,
                    "depth_mm": depth,
                    "units_width": result.units_width,
                    "units_depth": result.units_depth,
                    "split_count": len(splits),
                }
                add_component_to_config(active_project, component)
                print_success(f"Added to project: {active_project}")

            else:
                # Generate single baseplate (original behavior)
                if needs_split:
                    print_warning("Proceeding with single oversized baseplate...")
                    print()

                baseplate_path = project_path / f"{component_name}-baseplate.stl"
                spacer_path = project_path / f"{component_name}-spacers.stl"

                result = generate_drawer_fit(width, depth, baseplate_path, spacer_path)

                # Display calculation summary
                _display_drawer_fit_summary(result, width, depth, MIN_SPACER_GAP_MM)

                # Check spacer dimensions against print bed
                if result.spacer_path:
                    if width > PRINT_BED_WIDTH_MM or depth > PRINT_BED_DEPTH_MM:
                        print_warning(
                            f"Warning: Spacer dimensions may exceed print bed "
                            f"({PRINT_BED_WIDTH_MM}x{PRINT_BED_DEPTH_MM}mm)"
                        )
                        print()

                if needs_split:
                    print_success(
                        f"Generated baseplate: {result.baseplate_path} "
                        f"(WARNING: exceeds print bed)"
                    )
                else:
                    print_success(f"Generated baseplate: {result.baseplate_path}")

                if result.spacer_path:
                    print_success(f"Generated spacers: {result.spacer_path}")
                else:
                    print("No spacers generated (gaps below 4mm threshold)")

                # Add component to config
                component = {
                    "name": component_name,
                    "type": "drawer-fit",
                    "width_mm": width,
                    "depth_mm": depth,
                    "units_width": result.units_width,
                    "units_depth": result.units_depth,
                }
                add_component_to_config(active_project, component)
                print_success(f"Added to project: {active_project}")

        except ValueError as e:
            print_error(f"Invalid dimensions: {e}")
            sys.exit(1)
        except Exception as e:
            print_error(f"Generation failed: {e}")
            sys.exit(1)
    else:
        # Default behavior: save to output directory
        output_path = Path(output)

        try:
            if should_split:
                # Generate split baseplates
                print_header("Generating split baseplates...")
                splits = calculate_baseplate_splits(units_width, units_depth)
                baseplate_paths = generate_split_baseplates(
                    splits, output_path.parent, "baseplate"
                )

                # Display generated pieces
                for i, (path, (split_w, split_d)) in enumerate(
                    zip(baseplate_paths, splits), start=1
                ):
                    print_success(
                        f"  Generated {path.name} ({split_w}x{split_d} units)"
                    )

                # Generate spacers
                spacer_path = output_path.parent / f"{output_path.name}-spacers.stl"
                from gridfinity_invoke.generators import DrawerFitResult

                # Calculate gaps for spacer generation
                actual_width_mm = float(units_width * GRIDFINITY_UNIT_MM)
                actual_depth_mm = float(units_depth * GRIDFINITY_UNIT_MM)
                gap_x_mm = width - actual_width_mm
                gap_y_mm = depth - actual_depth_mm
                per_side_gap_x = gap_x_mm / 2
                per_side_gap_y = gap_y_mm / 2

                spacer_result_path = None
                if (
                    per_side_gap_x > MIN_SPACER_GAP_MM
                    or per_side_gap_y > MIN_SPACER_GAP_MM
                ):
                    from cqgridfinity import GridfinityDrawerSpacer

                    spacer_path.parent.mkdir(parents=True, exist_ok=True)
                    spacer = GridfinityDrawerSpacer(dr_width=width, dr_depth=depth)
                    spacer_obj = spacer.render_half_set()
                    if spacer_obj is not None:
                        spacer_obj.val().exportStl(
                            str(spacer_path)
                        )  # pyrefly: ignore[missing-attribute]
                        spacer_result_path = spacer_path

                # Create result object for display
                result = DrawerFitResult(
                    baseplate_path=baseplate_paths[0],
                    spacer_path=spacer_result_path,
                    units_width=units_width,
                    units_depth=units_depth,
                    actual_width_mm=actual_width_mm,
                    actual_depth_mm=actual_depth_mm,
                    gap_x_mm=gap_x_mm,
                    gap_y_mm=gap_y_mm,
                )

                # Display calculation summary
                _display_drawer_fit_summary(result, width, depth, MIN_SPACER_GAP_MM)

                # Check spacer dimensions against print bed
                if result.spacer_path:
                    if width > PRINT_BED_WIDTH_MM or depth > PRINT_BED_DEPTH_MM:
                        print_warning(
                            f"Warning: Spacer dimensions may exceed print bed "
                            f"({PRINT_BED_WIDTH_MM}x{PRINT_BED_DEPTH_MM}mm)"
                        )
                        print()

                if result.spacer_path:
                    print_success(f"Generated spacers: {result.spacer_path}")
                else:
                    print("No spacers generated (gaps below 4mm threshold)")

            else:
                # Generate single baseplate (original behavior)
                if needs_split:
                    print_warning("Proceeding with single oversized baseplate...")
                    print()

                baseplate_path = (
                    output_path.parent / f"{output_path.name}-baseplate.stl"
                )
                spacer_path = output_path.parent / f"{output_path.name}-spacers.stl"

                result = generate_drawer_fit(width, depth, baseplate_path, spacer_path)

                # Display calculation summary
                _display_drawer_fit_summary(result, width, depth, MIN_SPACER_GAP_MM)

                # Check spacer dimensions against print bed
                if result.spacer_path:
                    if width > PRINT_BED_WIDTH_MM or depth > PRINT_BED_DEPTH_MM:
                        print_warning(
                            f"Warning: Spacer dimensions may exceed print bed "
                            f"({PRINT_BED_WIDTH_MM}x{PRINT_BED_DEPTH_MM}mm)"
                        )
                        print()

                if needs_split:
                    print_success(
                        f"Generated baseplate: {result.baseplate_path} "
                        f"(WARNING: exceeds print bed)"
                    )
                else:
                    print_success(f"Generated baseplate: {result.baseplate_path}")

                if result.spacer_path:
                    print_success(f"Generated spacers: {result.spacer_path}")
                else:
                    print("No spacers generated (gaps below 4mm threshold)")

        except ValueError as e:
            print_error(f"Invalid dimensions: {e}")
            sys.exit(1)
        except Exception as e:
            print_error(f"Generation failed: {e}")
            sys.exit(1)


def _display_drawer_fit_summary(
    result: "DrawerFitResult",  # noqa: F821
    width: float,
    depth: float,
    min_spacer_gap_mm: float,
) -> None:
    """Display calculation summary for drawer-fit generation.

    Args:
        result: The DrawerFitResult from generate_drawer_fit
        width: Original drawer width in mm
        depth: Original drawer depth in mm
        min_spacer_gap_mm: Minimum gap threshold for spacer generation
    """
    print()
    print(f"Drawer: {width} x {depth} mm")
    print(f"Units: {result.units_width} x {result.units_depth}")
    print(f"Baseplate: {result.actual_width_mm} x {result.actual_depth_mm} mm")
    gap_x_per_side = result.gap_x_mm / 2
    gap_y_per_side = result.gap_y_mm / 2
    print(f"Gaps: X={gap_x_per_side}mm per side, Y={gap_y_per_side}mm per side")

    # Display spacer information
    per_side_gap_x = result.gap_x_mm / 2
    per_side_gap_y = result.gap_y_mm / 2

    spacers_to_generate = []
    if per_side_gap_x > min_spacer_gap_mm and per_side_gap_y > min_spacer_gap_mm:
        spacers_to_generate.extend(["corner", "front/back", "left/right"])
    elif per_side_gap_x > min_spacer_gap_mm:
        spacers_to_generate.append("left/right")
    elif per_side_gap_y > min_spacer_gap_mm:
        spacers_to_generate.append("front/back")

    if spacers_to_generate:
        print(f"Spacers: {', '.join(spacers_to_generate)}")
    else:
        print("Spacers: none needed (gaps too small)")

    print()


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
    from gridfinity_invoke.generators import (
        generate_baseplate,
        generate_bin,
        generate_drawer_fit,
    )
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

        if component_type == "bin":
            length = component["length"]
            width = component["width"]
            height = component["height"]
            output_path = project_path / f"{component_name}.stl"
            print(f"  Generating bin: {component_name} ({length}x{width}x{height})")
            generate_bin(length, width, height, output_path)
        elif component_type == "baseplate":
            length = component["length"]
            width = component["width"]
            output_path = project_path / f"{component_name}.stl"
            print(f"  Generating baseplate: {component_name} ({length}x{width})")
            generate_baseplate(length, width, output_path)
        elif component_type == "drawer-fit":
            width_mm = component["width_mm"]
            depth_mm = component["depth_mm"]
            baseplate_path = project_path / f"{component_name}-baseplate.stl"
            spacer_path = project_path / f"{component_name}-spacers.stl"
            print(
                f"  Generating drawer-fit: {component_name} ({width_mm}x{depth_mm}mm)"
            )
            generate_drawer_fit(width_mm, depth_mm, baseplate_path, spacer_path)

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
