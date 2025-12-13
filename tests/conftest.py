"""Pytest configuration for test suite."""

import pytest


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
