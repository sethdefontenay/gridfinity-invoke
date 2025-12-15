# Specification: BDD Scenarios Documentation

## Goal
Add pytest-bdd framework integration with Gherkin feature files documenting expected CLI behaviors, and establish a GitHub Actions CI workflow to automatically run both unit tests and BDD tests on pull requests.

## User Stories
- As a developer, I want BDD feature files documenting CLI behaviors so that I can understand expected functionality in human-readable format
- As a contributor, I want automated CI testing on pull requests so that regressions are caught before merging

## Specific Requirements

**pytest-bdd Framework Integration**
- Add pytest-bdd to dev dependencies in pyproject.toml
- Configure pytest to discover and run .feature files alongside existing unit tests
- Create step definition modules that invoke CLI commands and verify outputs
- Reuse existing fixtures from conftest.py where applicable (temp directories, mocking patterns)

**Feature File Organization**
- Create tests/features/ directory for all .feature files
- Create tests/step_defs/ directory for step definition Python modules
- One .feature file per gf.* command (7 total)
- Step definitions can be shared across feature files where patterns overlap

**baseplate.feature Scenarios**
- Happy path: generate baseplate with default dimensions (4x4)
- Happy path: generate baseplate with custom dimensions
- Error handling: dimensions less than 1 unit
- Project-aware: baseplate added to active project config
- Project-aware: STL saved to project directory

**bin.feature Scenarios**
- Happy path: generate bin with default dimensions (2x2x3)
- Happy path: generate bin with custom dimensions
- Error handling: dimensions less than 1 unit
- Project-aware: bin added to active project config
- Project-aware: STL saved to project directory

**drawer_fit.feature Scenarios**
- Happy path: generate drawer-fit with valid dimensions
- Calculation verification: correct unit counts and gaps displayed
- Error handling: width below 42mm minimum
- Error handling: depth below 42mm minimum
- Error handling: negative dimensions
- Warning display: baseplate exceeds print bed
- Split prompt: interactive split suggestion when oversized

**new_project.feature Scenarios**
- Happy path: create new project with directory and config.json
- Happy path: new project automatically set as active
- Error handling: project name already exists

**load.feature Scenarios**
- Happy path: load project and regenerate all STL files
- Happy path: loaded project set as active
- Error handling: project does not exist
- Component regeneration: bins, baseplates, and drawer-fit components

**list_projects.feature Scenarios**
- Happy path: display all projects with active indicator
- Empty state: "No projects found" when no projects exist

**config.feature Scenarios**
- Happy path: initialize config with --init flag
- Happy path: display config with --show flag
- Error handling: no flags provided shows usage error
- Display verification: max gridfinity units calculated correctly

**GitHub Actions CI Workflow**
- Create .github/workflows/test.yml workflow file
- Use actions/checkout@v4 for repository checkout
- Use actions/setup-python@v5 with Python 3.11
- Use pip caching via setup-python cache parameter
- Run pytest with JUnit XML output for GitHub test summary
- Generate coverage reports in Cobertura format
- Trigger on pull_request events to main/master branches
- Trigger on push events to main/master branches

## Visual Design
No visual assets provided.

## Existing Code to Leverage

**tests/conftest.py - Pytest Configuration**
- Custom markers defined (serial) that should be extended for BDD
- subprocess_lock fixture pattern for resource-intensive tests
- sys.path configuration for imports can be reused

**tests/test_drawer_fit_task.py - Fixture Patterns**
- temp_output_dir fixture pattern with isolated project state
- Patching of projects.PROJECTS_DIR, projects.ACTIVE_FILE, config.CONFIG_FILE
- MockContext from invoke for simulating CLI context
- capsys fixture usage for capturing stdout/stderr output

**tests/test_project_tasks.py - Project Management Patterns**
- temp_project_dir fixture for isolated project testing
- Pattern for creating projects and verifying config.json structure
- Active project verification using projects.get_active_project()

**tests/test_config_command.py - Subprocess Testing**
- subprocess.run pattern for full CLI integration tests
- Capture and verify both stdout and stderr
- Exit code verification for success/failure cases

**pyproject.toml - Test Configuration**
- pytest.ini_options with testpaths and addopts
- Coverage configuration (--cov=src/gridfinity_invoke)
- Custom markers registration pattern

## Out of Scope
- dev.lint command scenarios
- dev.format command scenarios
- dev.test command scenarios
- dev.check command scenarios
- pp command (pretty printing) scenarios
- Any other development/tooling commands
- Performance benchmarking tests
- Visual regression testing
- End-to-end browser testing
- Docker container testing
- Multi-Python-version matrix testing
