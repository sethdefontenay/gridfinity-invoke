Feature: Project Loading
    As a user
    I want to load existing Gridfinity projects
    So that I can continue working on them

    Scenario: Load project and regenerate all STL files
        Given an existing project named "load-test" with components
        When I load the project "load-test"
        Then the STL files should be regenerated
        And the exit code should be 0

    Scenario: Loaded project set as active
        Given an existing project named "set-active-test" with components
        When I load the project "set-active-test"
        Then the project should be set as active
        And the exit code should be 0

    Scenario: Error when project does not exist
        Given no projects exist
        When I try to load the project "nonexistent"
        Then the exit code should be 1
        And the output should contain "does not exist"

    Scenario: Component regeneration for bins and baseplates
        Given an existing project named "component-test" with mixed components
        When I load the project "component-test"
        Then both bin and baseplate STL files should exist
        And the exit code should be 0
