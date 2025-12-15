"""Tests for pytest-bdd framework setup verification."""

from pytest_bdd import given, scenarios, then, when

scenarios("../features/framework_test.feature")


@given("the pytest-bdd framework is installed")
def framework_installed():
    """Verify pytest-bdd is installed and importable."""
    import pytest_bdd

    assert pytest_bdd is not None


@when("I run a simple scenario")
def run_simple_scenario(scenario_context):
    """Mark that we're executing a scenario."""
    scenario_context["executed"] = True


@then("the scenario completes successfully")
def scenario_completes(scenario_context):
    """Verify the scenario completed."""
    assert scenario_context.get("executed") is True


def test_pytest_bdd_is_installed():
    """Test that pytest-bdd package is installed and importable."""
    from importlib.metadata import version

    pytest_bdd_version = version("pytest-bdd")
    assert pytest_bdd_version is not None


def test_feature_files_directory_exists():
    """Test that tests/features/ directory exists."""
    from pathlib import Path

    features_dir = Path(__file__).parent.parent / "features"
    assert features_dir.exists()
    assert features_dir.is_dir()


def test_step_defs_directory_exists():
    """Test that tests/step_defs/ directory exists."""
    from pathlib import Path

    step_defs_dir = Path(__file__).parent
    assert step_defs_dir.exists()
    assert step_defs_dir.is_dir()
    assert (step_defs_dir / "__init__.py").exists()
