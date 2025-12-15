Feature: Bin Generation
    As a user
    I want to generate Gridfinity bins
    So that I can store items in my baseplates

    Scenario: Generate bin with default dimensions
        Given a clean output directory
        When I generate a bin with default dimensions
        Then the bin STL file should exist
        And the exit code should be 0

    Scenario: Generate bin with custom dimensions
        Given a clean output directory
        When I generate a bin with length 3, width 2, and height 4
        Then the bin STL file should exist
        And the exit code should be 0

    Scenario: Error when dimensions less than 1 unit
        Given a clean output directory
        When I generate a bin with length 0, width 2, and height 3
        Then the exit code should be 1
        And the output should contain "positive integers"

    Scenario: Bin added to active project config
        Given an active project named "bin-test"
        When I generate a bin with length 2, width 2, and height 3
        Then the project config should contain a bin component
        And the component should have length 2, width 2, and height 3

    Scenario: STL saved to project directory
        Given an active project named "bin-stl-test"
        When I generate a bin with length 1, width 1, and height 2
        Then the bin STL should exist in the project directory
