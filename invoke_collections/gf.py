"""Gridfinity tasks collection for gridfinity-invoke project."""

import sys
from pathlib import Path

from invoke import Collection, task
from invoke.context import Context

from invoke_collections.helpers import (
    print_error,
    print_header,
    print_success,
    print_warning,
    prompt_with_default,
)


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
    from gridfinity_invoke.config import ensure_printer_config
    from gridfinity_invoke.generators import (
        GRIDFINITY_UNIT_MM,
        MIN_SPACER_GAP_MM,
        calculate_baseplate_splits,
        generate_drawer_fit,
        generate_split_baseplates,
        get_max_units,
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
    print()

    # Ensure printer config exists (prompt if missing, log if exists)
    ensure_printer_config()
    print()

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

    # Get max units from config
    max_units_x, max_units_y = get_max_units()

    # Check if splitting is needed
    needs_split = units_width > max_units_x or units_depth > max_units_y
    should_split = False

    # Print bed constraint warnings and interactive splitting prompt
    if needs_split:
        from gridfinity_invoke.config import get_print_bed_dimensions

        bed_width, bed_depth = get_print_bed_dimensions()
        actual_width_mm = units_width * GRIDFINITY_UNIT_MM
        actual_depth_mm = units_depth * GRIDFINITY_UNIT_MM
        print_warning(
            f"Warning: Calculated baseplate ({units_width}x{units_depth} units = "
            f"{actual_width_mm}x{actual_depth_mm}mm) exceeds print bed "
            f"({bed_width}x{bed_depth}mm)"
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
                    from gridfinity_invoke.config import get_print_bed_dimensions

                    bed_width, bed_depth = get_print_bed_dimensions()
                    if width > bed_width or depth > bed_depth:
                        print_warning(
                            f"Warning: Spacer dimensions may exceed print bed "
                            f"({bed_width}x{bed_depth}mm)"
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
                    from gridfinity_invoke.config import get_print_bed_dimensions

                    bed_width, bed_depth = get_print_bed_dimensions()
                    if width > bed_width or depth > bed_depth:
                        print_warning(
                            f"Warning: Spacer dimensions may exceed print bed "
                            f"({bed_width}x{bed_depth}mm)"
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
                    from gridfinity_invoke.config import get_print_bed_dimensions

                    bed_width, bed_depth = get_print_bed_dimensions()
                    if width > bed_width or depth > bed_depth:
                        print_warning(
                            f"Warning: Spacer dimensions may exceed print bed "
                            f"({bed_width}x{bed_depth}mm)"
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
                    from gridfinity_invoke.config import get_print_bed_dimensions

                    bed_width, bed_depth = get_print_bed_dimensions()
                    if width > bed_width or depth > bed_depth:
                        print_warning(
                            f"Warning: Spacer dimensions may exceed print bed "
                            f"({bed_width}x{bed_depth}mm)"
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


@task
def config(ctx: Context, init: bool = False, show: bool = False) -> None:
    """{"desc": "Manage printer configuration", "params": [{"name": "init", "type": "bool", "desc": "Initialize or update printer dimensions interactively", "example": "true"}, {"name": "show", "type": "bool", "desc": "Display current configuration values", "example": "true"}], "returns": {}}"""  # noqa: E501
    from gridfinity_invoke.config import (
        DEFAULT_BED_DEPTH,
        DEFAULT_BED_WIDTH,
        load_printer_config,
        save_printer_config,
    )

    # Require at least one flag
    if not init and not show:
        print_error("Error: At least one flag is required")
        print()
        print("Usage:")
        print("  inv gf.config --init    # Initialize or update printer dimensions")
        print("  inv gf.config --show    # Display current configuration")
        sys.exit(1)

    if init:
        print_header("Printer Configuration Setup")
        print()
        print("Enter your printer's bed dimensions in millimeters.")
        print()

        # Prompt for dimensions with defaults
        width_str = prompt_with_default("Print bed width (mm)", str(DEFAULT_BED_WIDTH))
        depth_str = prompt_with_default("Print bed depth (mm)", str(DEFAULT_BED_DEPTH))

        # Convert to integers
        try:
            width = int(width_str)
            depth = int(depth_str)
        except ValueError:
            print_error("Error: Dimensions must be integers")
            sys.exit(1)

        # Save configuration
        config = {
            "print_bed_width_mm": width,
            "print_bed_depth_mm": depth,
        }
        save_printer_config(config)

        print()
        print_success("Configuration saved to .gf-config")
        print_success(f"Print bed: {width}mm x {depth}mm")

    if show:
        print_header("Current Printer Configuration")
        print()

        config = load_printer_config()
        width = config["print_bed_width_mm"]
        depth = config["print_bed_depth_mm"]

        print(f"Print bed width:  {width}mm")
        print(f"Print bed depth:  {depth}mm")
        print()

        # Calculate max gridfinity units
        GRIDFINITY_UNIT_MM = 42  # Standard gridfinity unit size
        max_units_x = width // GRIDFINITY_UNIT_MM
        max_units_y = depth // GRIDFINITY_UNIT_MM

        print(f"Max gridfinity units: {max_units_x} x {max_units_y}")
        print()


# Create the gf collection
gf = Collection("gf")
gf.add_task(bin)
gf.add_task(baseplate)
gf.add_task(drawer_fit)
gf.add_task(new_project)
gf.add_task(load)
gf.add_task(list_projects)
gf.add_task(config)
