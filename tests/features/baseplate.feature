Feature: Baseplate Generation
    As a user
    I want to generate Gridfinity baseplates
    So that I can organize items in my drawers

    Scenario: Generate baseplate with default dimensions
        Given a clean output directory
        When I generate a baseplate with default dimensions
        Then the baseplate STL file should exist
        And the exit code should be 0

    Scenario: Generate baseplate with custom dimensions
        Given a clean output directory
        When I generate a baseplate with length 3 and width 5
        Then the baseplate STL file should exist
        And the exit code should be 0

    Scenario: Error when dimensions less than 1 unit
        Given a clean output directory
        When I generate a baseplate with length 0 and width 4
        Then the exit code should be 1
        And the output should contain "positive integers"

    Scenario: Baseplate added to active project config
        Given an active project named "baseplate-test"
        When I generate a baseplate with length 4 and width 4
        Then the project config should contain a baseplate component
        And the component should have length 4 and width 4

    Scenario: STL saved to project directory
        Given an active project named "baseplate-stl-test"
        When I generate a baseplate with length 2 and width 2
        Then the baseplate STL should exist in the project directory
