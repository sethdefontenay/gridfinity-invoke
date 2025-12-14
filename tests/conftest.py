"""Pytest configuration for test suite."""

import sys
from pathlib import Path

import pytest

# Add the repository root to sys.path so that tasks.py can be imported
repo_root = Path(__file__).parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "serial: mark test to run serially (not in parallel with other tests)",
    )


# Use a module-scoped lock to ensure subprocess-heavy tests don't overwhelm resources
@pytest.fixture(scope="session")
def subprocess_lock() -> None:
    """Fixture to indicate tests that run subprocesses.

    Tests using this fixture signal they are resource-intensive.
    When using pytest-xdist, configure with --dist=loadfile to group
    tests by file and reduce parallel subprocess spawning.
    """
    pass
