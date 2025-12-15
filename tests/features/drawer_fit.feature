Feature: Drawer Fit Solution
    As a user
    I want to generate drawer-fit solutions
    So that my baseplates fit perfectly in my drawer dimensions

    Scenario: Generate drawer-fit with valid dimensions
        Given a clean output directory
        When I generate a drawer-fit with width 200 and depth 200
        Then the drawer-fit baseplate STL file should exist
        And the exit code should be 0

    Scenario: Calculation verification - correct unit counts displayed
        Given a clean output directory
        When I generate a drawer-fit with width 200 and depth 200
        Then the output should contain "4"
        And the exit code should be 0

    Scenario: Error when width below 42mm minimum
        Given a clean output directory
        When I generate a drawer-fit with width 30 and depth 200
        Then the exit code should be 1
        And the output should contain "42"

    Scenario: Error when depth below 42mm minimum
        Given a clean output directory
        When I generate a drawer-fit with width 200 and depth 30
        Then the exit code should be 1
        And the output should contain "42"

    Scenario: Error when negative dimensions provided
        Given a clean output directory
        When I generate a drawer-fit with width -100 and depth 200
        Then the exit code should be 1
        And the output should contain "positive"

    Scenario: Warning displayed when baseplate exceeds print bed
        Given a clean output directory
        When I generate an oversized drawer-fit with width 300 and depth 300
        Then the output should contain "Warning"
        And the exit code should be 0

    Scenario: Split prompt for oversized baseplates
        Given a clean output directory
        When I generate an oversized drawer-fit with width 300 and depth 300 declining split
        Then the output should contain "split"
        And the exit code should be 0
