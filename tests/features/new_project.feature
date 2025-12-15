Feature: New Project Creation
    As a user
    I want to create new Gridfinity projects
    So that I can organize my components into projects

    Scenario: Create new project with directory and config.json
        Given no projects exist
        When I create a new project named "my-project"
        Then the project directory should exist
        And the project config.json should exist
        And the exit code should be 0

    Scenario: New project automatically set as active
        Given no projects exist
        When I create a new project named "auto-active-project"
        Then the project should be set as active
        And the exit code should be 0

    Scenario: Error when project name already exists
        Given no projects exist
        When I create a new project named "duplicate"
        And I try to create another project named "duplicate"
        Then the exit code should be 1
        And the output should contain "already exists"
