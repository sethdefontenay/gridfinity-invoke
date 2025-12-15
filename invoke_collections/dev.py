"""Development tasks collection for gridfinity-invoke project."""

import sys

from invoke import Collection, task
from invoke.context import Context

from invoke_collections.helpers import print_error, print_header, print_success


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


# Create the dev collection
dev = Collection("dev")
dev.add_task(lint)
dev.add_task(format)
dev.add_task(test)
dev.add_task(check)
