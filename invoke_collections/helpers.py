"""Shared helper functions for invoke tasks."""

import json

from colorama import Fore, Style


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
