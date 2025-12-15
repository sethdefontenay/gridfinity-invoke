"""Printer configuration module for Gridfinity projects.

Handles printer bed dimensions and configuration persistence.
"""

import json
from pathlib import Path

# Configuration file and defaults
CONFIG_FILE = Path(".gf-config")
DEFAULT_BED_WIDTH = 225
DEFAULT_BED_DEPTH = 225


def load_printer_config() -> dict:
    """Load printer configuration from .gf-config file.

    Returns:
        Dictionary with print_bed_width_mm and print_bed_depth_mm keys.
        Returns defaults if file doesn't exist.
    """
    try:
        config_data = json.loads(CONFIG_FILE.read_text())
        return config_data
    except FileNotFoundError:
        return {
            "print_bed_width_mm": DEFAULT_BED_WIDTH,
            "print_bed_depth_mm": DEFAULT_BED_DEPTH,
        }


def save_printer_config(config: dict) -> None:
    """Save printer configuration to .gf-config file.

    Args:
        config: Dictionary with printer configuration values.
    """
    CONFIG_FILE.write_text(json.dumps(config, indent=2))


def get_print_bed_dimensions() -> tuple[int, int]:
    """Get print bed dimensions from configuration.

    Returns:
        Tuple of (width_mm, depth_mm) as integers.
    """
    config = load_printer_config()
    return (
        config["print_bed_width_mm"],
        config["print_bed_depth_mm"],
    )


def ensure_printer_config() -> None:
    """Ensure printer configuration exists, prompting user if missing.

    If .gf-config file doesn't exist, interactively prompts the user
    for printer dimensions and saves them to the config file.
    If config already exists, uses it silently and logs a message.
    """
    # Check if config file exists
    if CONFIG_FILE.exists():
        # Config exists, use it silently
        config = load_printer_config()
        width = config["print_bed_width_mm"]
        depth = config["print_bed_depth_mm"]
        print(f"Using printer config: {width}mm x {depth}mm print bed")
        return

    # Config missing, prompt user
    from invoke_collections.helpers import (
        print_header,
        print_success,
        prompt_with_default,
    )

    print()
    print_header("Printer Configuration Required")
    print()
    print("This command needs your printer's bed dimensions.")
    print("Enter the dimensions in millimeters (default: 225mm for both).")
    print()

    # Prompt for dimensions
    width_str = prompt_with_default("Print bed width (mm)", str(DEFAULT_BED_WIDTH))
    depth_str = prompt_with_default("Print bed depth (mm)", str(DEFAULT_BED_DEPTH))

    # Convert to integers
    width = int(width_str)
    depth = int(depth_str)

    # Save configuration
    config = {
        "print_bed_width_mm": width,
        "print_bed_depth_mm": depth,
    }
    save_printer_config(config)

    print()
    print_success("Configuration saved to .gf-config")
    print_success(f"Print bed: {width}mm x {depth}mm")
    print()
