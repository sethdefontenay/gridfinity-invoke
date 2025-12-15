#!/bin/bash
set -e

# ============================================================================
# Gridfinity Invoke Installation Script
# ============================================================================
# This script sets up the development environment for gridfinity-invoke:
# - Creates a Python virtual environment
# - Installs project dependencies from pyproject.toml
# - Runs lint checks to verify code quality
# - Runs test suite to verify functionality
# ============================================================================

echo "=========================================="
echo "Gridfinity Invoke - Installation Script"
echo "=========================================="
echo ""

# Detect Python command (python3 vs python)
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.11 or later and try again."
    exit 1
fi

echo "Using Python: $PYTHON_CMD ($(${PYTHON_CMD} --version))"
echo ""

# Step 1: Create virtual environment
echo "Step 1/4: Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "  WARNING: .venv directory already exists. Skipping virtualenv creation."
    echo "  To recreate, delete .venv and run this script again."
else
    ${PYTHON_CMD} -m venv .venv
    echo "  Virtual environment created successfully."
fi
echo ""

# Activate virtual environment
echo "  Activating virtual environment..."
source .venv/bin/activate
echo "  Virtual environment activated."
echo ""

# Step 2: Install dependencies
echo "Step 2/4: Installing dependencies..."
echo "  Installing core dependencies from pyproject.toml..."
pip install -e . --quiet
echo "  Core dependencies installed."

# Install dev dependencies if they exist in pyproject.toml
if grep -q "project.optional-dependencies" pyproject.toml 2>/dev/null; then
    echo "  Installing development dependencies..."
    pip install -e ".[dev]" --quiet
    echo "  Development dependencies installed."
fi
echo ""

# Step 3: Run lint check
echo "Step 3/4: Running lint check..."
if inv dev.lint; then
    echo "  Lint check passed!"
else
    echo ""
    echo "ERROR: Lint check failed!"
    echo ""
    echo "Troubleshooting hints:"
    echo "  - Run 'inv dev.lint' to see detailed linting errors"
    echo "  - Run 'inv dev.format' to auto-format code"
    echo "  - Fix any remaining issues manually"
    exit 1
fi
echo ""

# Step 4: Run tests
echo "Step 4/4: Running tests..."
if inv dev.test; then
    echo "  Tests passed!"
else
    echo ""
    echo "ERROR: Tests failed!"
    echo ""
    echo "Troubleshooting hints:"
    echo "  - Run 'inv dev.test --verbose' to see detailed test output"
    echo "  - Check test failures and fix code as needed"
    echo "  - Ensure all dependencies are installed correctly"
    exit 1
fi
echo ""

# Success summary
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment:"
echo "     source .venv/bin/activate"
echo ""
echo "  2. Configure your printer dimensions (optional):"
echo "     inv gf.config --init"
echo ""
echo "  3. View all available commands:"
echo "     inv pp"
echo ""
echo "  4. Generate your first Gridfinity component:"
echo "     inv gf.baseplate --width=3 --depth=3"
echo ""
