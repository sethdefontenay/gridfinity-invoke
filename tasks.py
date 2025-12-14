"""Invoke tasks for gridfinity-invoke project."""

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
    """
    {
        "desc": "Run ruff formatter on source and test files",
        "params": [
            {
                "name": "check",
                "type": "bool",
                "desc": "Check formatting without modifying files (CI mode)",
                "example": "true"
            }
        ],
        "returns": {}
    }
    """
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
    """
    {
        "desc": "Run pytest with coverage reporting",
        "params": [
            {
                "name": "verbose",
                "type": "bool",
                "desc": "Enable verbose output",
                "example": "true"
            }
        ],
        "returns": {}
    }
    """
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
    """
    {
        "desc": "Run lint and test in sequence, failing fast on lint errors",
        "params": [],
        "returns": {}
    }
    """
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
    """
    {
        "desc": "Generate a Gridfinity bin and export to STL",
        "params": [
            {
                "name": "length",
                "type": "int",
                "desc": "Length in gridfinity units (1 unit = 42mm)",
                "example": "2"
            },
            {
                "name": "width",
                "type": "int",
                "desc": "Width in gridfinity units",
                "example": "2"
            },
            {
                "name": "height",
                "type": "int",
                "desc": "Height in gridfinity units (1 unit = 7mm)",
                "example": "3"
            },
            {
                "name": "output",
                "type": "string",
                "desc": "Output path for the STL file",
                "example": "output/bin.stl"
            }
        ],
        "returns": {}
    }
    """
    from gridfinity_invoke.generators import generate_bin

    print_header(f"Generating {length}x{width}x{height} Gridfinity bin...")

    if length < 1 or width < 1 or height < 1:
        print_error("All dimensions must be positive integers >= 1")
        sys.exit(1)

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
    """
    {
        "desc": "Generate a Gridfinity baseplate and export to STL",
        "params": [
            {
                "name": "length",
                "type": "int",
                "desc": "Length in gridfinity units (1 unit = 42mm)",
                "example": "4"
            },
            {
                "name": "width",
                "type": "int",
                "desc": "Width in gridfinity units",
                "example": "4"
            },
            {
                "name": "output",
                "type": "string",
                "desc": "Output path for the STL file",
                "example": "output/baseplate.stl"
            }
        ],
        "returns": {}
    }
    """
    from gridfinity_invoke.generators import generate_baseplate

    print_header(f"Generating {length}x{width} Gridfinity baseplate...")

    if length < 1 or width < 1:
        print_error("All dimensions must be positive integers >= 1")
        sys.exit(1)

    try:
        result_path = generate_baseplate(length, width, output)
        print_success(f"Generated: {result_path}")
    except Exception as e:
        print_error(f"Generation failed: {e}")
        sys.exit(1)
