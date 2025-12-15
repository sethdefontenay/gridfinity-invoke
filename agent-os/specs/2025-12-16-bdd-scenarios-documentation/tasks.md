# Task Breakdown: BDD Scenarios Documentation

## Overview
Total Tasks: 28 (across 5 task groups)

## Task List

### Infrastructure Layer

#### Task Group 1: pytest-bdd Framework Setup
**Dependencies:** None

- [x] 1.0 Complete pytest-bdd framework integration
  - [x] 1.1 Write 2-4 focused tests for pytest-bdd configuration
    - Test that pytest discovers .feature files in tests/features/
    - Test that step definitions in tests/step_defs/ are loaded
    - Test that pytest-bdd integrates with existing pytest fixtures
  - [x] 1.2 Add pytest-bdd to dev dependencies in pyproject.toml
    - Add "pytest-bdd" to [project.optional-dependencies] dev list
  - [x] 1.3 Create tests/features/ directory structure
    - Create empty tests/features/ directory for .feature files
  - [x] 1.4 Create tests/step_defs/ directory structure
    - Create empty tests/step_defs/ directory for step definition modules
    - Create tests/step_defs/__init__.py
  - [x] 1.5 Update pytest configuration in pyproject.toml
    - Add bdd_features_base_dir setting to [tool.pytest.ini_options]
    - Ensure testpaths includes feature discovery
  - [x] 1.6 Create tests/step_defs/conftest.py with shared fixtures
    - Import and expose temp_output_dir fixture pattern from existing tests
    - Import and expose temp_project_dir fixture pattern
    - Create cli_runner fixture for subprocess-based CLI invocation
    - Create isolated_config fixture for config file isolation
  - [x] 1.7 Ensure framework setup tests pass
    - Run ONLY the 2-4 tests written in 1.1
    - Verify pytest-bdd is installed and discoverable
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 2-4 tests written in 1.1 pass
- pytest-bdd is installed via pip install -e ".[dev]"
- Directory structure exists: tests/features/, tests/step_defs/
- Shared fixtures are available for step definitions
- pytest configuration properly discovers .feature files

---

### Core Command Features (Group A)

#### Task Group 2: baseplate and bin Feature Files
**Dependencies:** Task Group 1

- [x] 2.0 Complete baseplate.feature and bin.feature with step definitions
  - [x] 2.1 Write 4-6 focused tests validating feature file execution
    - Test baseplate happy path scenario runs successfully
    - Test baseplate error handling scenario (dimensions < 1 unit)
    - Test bin happy path scenario runs successfully
    - Test bin error handling scenario (dimensions < 1 unit)
  - [x] 2.2 Create tests/features/baseplate.feature
    - Feature: Baseplate Generation
    - Scenario: Generate baseplate with default dimensions (4x4)
    - Scenario: Generate baseplate with custom dimensions
    - Scenario: Error when dimensions less than 1 unit
    - Scenario: Baseplate added to active project config
    - Scenario: STL saved to project directory
  - [x] 2.3 Create tests/features/bin.feature
    - Feature: Bin Generation
    - Scenario: Generate bin with default dimensions (2x2x3)
    - Scenario: Generate bin with custom dimensions
    - Scenario: Error when dimensions less than 1 unit
    - Scenario: Bin added to active project config
    - Scenario: STL saved to project directory
  - [x] 2.4 Create tests/step_defs/test_baseplate_steps.py
    - Implement Given steps for environment setup
    - Implement When steps for invoking gf.baseplate command
    - Implement Then steps for output and file verification
    - Use subprocess.run pattern from test_config_command.py
  - [x] 2.5 Create tests/step_defs/test_bin_steps.py
    - Implement Given steps for environment setup
    - Implement When steps for invoking gf.bin command
    - Implement Then steps for output and file verification
    - Reuse common step patterns from baseplate steps where applicable
  - [x] 2.6 Create tests/step_defs/common_steps.py for shared step definitions
    - Common Given steps: "a clean output directory", "an active project"
    - Common Then steps: "the STL file should exist", "the exit code should be {code}"
  - [x] 2.7 Ensure baseplate and bin feature tests pass
    - Run ONLY the 4-6 tests written in 2.1
    - Verify all scenarios execute successfully
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 4-6 tests written in 2.1 pass
- baseplate.feature contains 5 scenarios
- bin.feature contains 5 scenarios
- Step definitions properly invoke CLI and verify outputs
- Common steps are shared between features

---

### Core Command Features (Group B)

#### Task Group 3: drawer-fit and config Feature Files
**Dependencies:** Task Group 1

- [x] 3.0 Complete drawer_fit.feature and config.feature with step definitions
  - [x] 3.1 Write 4-6 focused tests validating feature file execution
    - Test drawer-fit happy path scenario runs successfully
    - Test drawer-fit error handling scenario (width < 42mm)
    - Test config --show scenario runs successfully
    - Test config no-flags error scenario
  - [x] 3.2 Create tests/features/drawer_fit.feature
    - Feature: Drawer Fit Solution
    - Scenario: Generate drawer-fit with valid dimensions
    - Scenario: Calculation verification - correct unit counts and gaps displayed
    - Scenario: Error when width below 42mm minimum
    - Scenario: Error when depth below 42mm minimum
    - Scenario: Error when negative dimensions provided
    - Scenario: Warning displayed when baseplate exceeds print bed
    - Scenario Outline: Split prompt for oversized baseplates (with mocked input)
  - [x] 3.3 Create tests/features/config.feature
    - Feature: Printer Configuration
    - Scenario: Initialize config with --init flag
    - Scenario: Display config with --show flag
    - Scenario: Error when no flags provided
    - Scenario: Max gridfinity units calculated correctly
  - [x] 3.4 Create tests/step_defs/test_drawer_fit_steps.py
    - Implement Given steps for drawer dimensions setup
    - Implement When steps for invoking gf.drawer-fit command
    - Implement Then steps for calculation and warning verification
    - Handle mocked input() for split prompt scenarios
  - [x] 3.5 Create tests/step_defs/test_config_steps.py
    - Implement Given steps for config file state
    - Implement When steps for invoking gf.config command with flags
    - Implement Then steps for output verification
    - Follow subprocess.run pattern from existing test_config_command.py
  - [x] 3.6 Ensure drawer-fit and config feature tests pass
    - Run ONLY the 4-6 tests written in 3.1
    - Verify all scenarios execute successfully
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 4-6 tests written in 3.1 pass
- drawer_fit.feature contains 7 scenarios
- config.feature contains 4 scenarios
- Step definitions handle mocked input for interactive prompts
- Error cases properly verified

---

### Project Management Features

#### Task Group 4: Project Management Feature Files
**Dependencies:** Task Group 1

- [x] 4.0 Complete project management features with step definitions
  - [x] 4.1 Write 4-6 focused tests validating feature file execution
    - Test new-project happy path scenario runs successfully
    - Test load project scenario runs successfully
    - Test list-projects scenario runs successfully
    - Test error scenarios for non-existent projects
  - [x] 4.2 Create tests/features/new_project.feature
    - Feature: New Project Creation
    - Scenario: Create new project with directory and config.json
    - Scenario: New project automatically set as active
    - Scenario: Error when project name already exists
  - [x] 4.3 Create tests/features/load.feature
    - Feature: Project Loading
    - Scenario: Load project and regenerate all STL files
    - Scenario: Loaded project set as active
    - Scenario: Error when project does not exist
    - Scenario: Component regeneration for bins, baseplates, and drawer-fit
  - [x] 4.4 Create tests/features/list_projects.feature
    - Feature: List Projects
    - Scenario: Display all projects with active indicator
    - Scenario: Empty state shows "No projects found"
  - [x] 4.5 Create tests/step_defs/test_project_steps.py
    - Implement Given steps for project directory setup
    - Implement When steps for invoking gf.new-project, gf.load, gf.list-projects
    - Implement Then steps for project state verification
    - Use temp_project_dir fixture pattern from existing tests
  - [x] 4.6 Ensure project management feature tests pass
    - Run ONLY the 4-6 tests written in 4.1
    - Verify all scenarios execute successfully
    - Do NOT run the entire test suite at this stage

**Acceptance Criteria:**
- The 4-6 tests written in 4.1 pass
- new_project.feature contains 3 scenarios
- load.feature contains 4 scenarios
- list_projects.feature contains 2 scenarios
- Project state isolation works correctly via fixtures

---

### CI/CD Layer

#### Task Group 5: GitHub Actions CI Workflow
**Dependencies:** Task Groups 1-4

- [x] 5.0 Complete GitHub Actions CI workflow setup
  - [x] 5.1 Write 2-4 focused validation checks for workflow file
    - Validate YAML syntax is correct
    - Validate workflow triggers are configured properly
    - Validate Python version matches project requirements (3.11)
    - Validate test command runs both unit and BDD tests
  - [x] 5.2 Create .github/workflows/ directory structure
    - Create .github/ directory if not exists
    - Create .github/workflows/ directory
  - [x] 5.3 Create .github/workflows/test.yml workflow file
    - Name: "Tests"
    - Trigger on: pull_request to main/master, push to main/master
    - Use actions/checkout@v4
    - Use actions/setup-python@v5 with Python 3.11
    - Enable pip caching via setup-python cache parameter
    - Install dev dependencies: pip install -e ".[dev]"
    - Run pytest with JUnit XML output: pytest --junitxml=test-results.xml
    - Run coverage in Cobertura format: pytest --cov --cov-report=xml
  - [x] 5.4 Add test results upload step
    - Use actions/upload-artifact@v4 for test results
    - Upload JUnit XML for GitHub test summary display
    - Upload coverage report for visibility
  - [x] 5.5 Add workflow status badge to README (optional)
    - Add badge markdown to project README if desired
  - [x] 5.6 Validate workflow locally
    - Use act or similar tool to test workflow locally if available
    - Verify pytest command runs all tests (unit + BDD)
    - Ensure workflow syntax is valid

**Acceptance Criteria:**
- The 2-4 validation checks from 5.1 pass
- .github/workflows/test.yml exists and is valid YAML
- Workflow triggers on PR and push to main/master
- pytest runs both unit tests and BDD feature tests
- Test results available in GitHub Actions UI

---

### Integration and Verification

#### Task Group 6: Test Review and Final Validation
**Dependencies:** Task Groups 1-5

- [x] 6.0 Review and validate complete BDD test suite
  - [x] 6.1 Review all tests from Task Groups 1-5
    - Review 2-4 framework setup tests from Task Group 1
    - Review 4-6 baseplate/bin tests from Task Group 2
    - Review 4-6 drawer-fit/config tests from Task Group 3
    - Review 4-6 project management tests from Task Group 4
    - Review 2-4 workflow validation checks from Task Group 5
    - Total existing tests: approximately 16-26 tests
  - [x] 6.2 Analyze test coverage gaps for BDD feature only
    - Identify any critical scenarios missing from feature files
    - Focus ONLY on gaps related to this spec's BDD requirements
    - Do NOT assess entire application test coverage
    - Check that all 7 feature files have executable scenarios
  - [x] 6.3 Write up to 6 additional strategic tests if needed
    - Add maximum of 6 new tests to fill identified critical gaps
    - Focus on integration between features (e.g., drawer-fit with active project)
    - Ensure step definitions are reusable across features
    - Do NOT write comprehensive coverage for all edge cases
  - [x] 6.4 Run all BDD-related tests
    - Run all feature tests: pytest tests/features/ -v
    - Run step definition tests
    - Expected total: approximately 20-32 tests maximum
    - Verify all scenarios pass
  - [x] 6.5 Verify GitHub Actions workflow integration
    - Confirm pytest discovers and runs all BDD tests
    - Verify workflow file passes syntax validation
    - Test local pytest run includes both unit and BDD tests

**Acceptance Criteria:**
- All BDD feature tests pass (approximately 20-32 tests total)
- All 7 feature files have passing executable scenarios
- Step definitions are properly shared where patterns overlap
- GitHub Actions workflow is ready for deployment
- pytest runs both unit tests and BDD tests with single command

---

## Execution Order

Recommended implementation sequence:

1. **Task Group 1: pytest-bdd Framework Setup** - Foundation for all BDD tests
2. **Task Groups 2, 3, 4 (parallel)** - Feature files can be developed independently after framework setup:
   - Task Group 2: baseplate and bin features
   - Task Group 3: drawer-fit and config features
   - Task Group 4: project management features
3. **Task Group 5: GitHub Actions CI Workflow** - Can begin after at least one feature group is complete
4. **Task Group 6: Test Review and Final Validation** - Requires all previous groups complete

## Feature File Summary

| Feature File | Command | Scenario Count |
|-------------|---------|----------------|
| baseplate.feature | gf.baseplate | 5 |
| bin.feature | gf.bin | 5 |
| drawer_fit.feature | gf.drawer-fit | 7 |
| config.feature | gf.config | 4 |
| new_project.feature | gf.new-project | 3 |
| load.feature | gf.load | 4 |
| list_projects.feature | gf.list-projects | 2 |
| edge_cases.feature | various | 4 |
| framework_test.feature | N/A | 1 |
| **Total** | | **35 scenarios** |

## Directory Structure After Implementation

```
gridfinity/
├── .github/
│   └── workflows/
│       └── test.yml
├── tests/
│   ├── conftest.py (existing)
│   ├── features/
│   │   ├── baseplate.feature
│   │   ├── bin.feature
│   │   ├── config.feature
│   │   ├── drawer_fit.feature
│   │   ├── edge_cases.feature
│   │   ├── framework_test.feature
│   │   ├── list_projects.feature
│   │   ├── load.feature
│   │   └── new_project.feature
│   ├── step_defs/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_baseplate_steps.py
│   │   ├── test_bin_steps.py
│   │   ├── test_config_steps.py
│   │   ├── test_drawer_fit_steps.py
│   │   ├── test_edge_cases_steps.py
│   │   ├── test_framework_setup.py
│   │   └── test_project_steps.py
│   └── (existing test files)
└── pyproject.toml (updated)
```

## Technical Notes

- **pytest-bdd version**: Use latest stable version compatible with Python 3.11+
- **Feature file naming**: Use snake_case to match Python module naming conventions
- **Step definition files**: Prefix with `test_` so pytest autodiscovers them
- **Fixture reuse**: Leverage existing temp_output_dir and temp_project_dir patterns
- **CLI invocation**: Use subprocess.run for full integration tests, MockContext for unit-level
- **GitHub Actions caching**: Use setup-python's built-in pip caching for faster CI runs

## Implementation Summary

All 6 task groups have been completed:

1. **Task Group 1**: pytest-bdd framework set up with 4 framework verification tests
2. **Task Group 2**: baseplate.feature (5 scenarios) and bin.feature (5 scenarios) with step definitions
3. **Task Group 3**: drawer_fit.feature (7 scenarios) and config.feature (4 scenarios) with step definitions
4. **Task Group 4**: new_project.feature (3 scenarios), load.feature (4 scenarios), and list_projects.feature (2 scenarios) with step definitions
5. **Task Group 5**: GitHub Actions CI workflow created at .github/workflows/test.yml
6. **Task Group 6**: Added edge_cases.feature (4 scenarios) for additional coverage

**Final test count: 38 BDD tests, all passing with 83% code coverage**
