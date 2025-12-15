Feature: Edge Cases and Error Handling
    As a user
    I want the system to handle edge cases gracefully
    So that I get clear error messages when things go wrong

    Scenario: Baseplate generation with exact print bed size
        Given a clean output directory
        When I generate a baseplate with length 5 and width 5
        Then the baseplate STL file should exist
        And the exit code should be 0

    Scenario: Bin generation with height of 1 unit
        Given a clean output directory
        When I generate a bin with length 1, width 1, and height 1
        Then the bin STL file should exist
        And the exit code should be 0

    Scenario: Drawer-fit with exact gridfinity unit multiples
        Given a clean output directory
        When I generate a drawer-fit with width 168 and depth 126
        Then the drawer-fit baseplate STL file should exist
        And the exit code should be 0

    Scenario: Show config displays correct max units
        Given a printer configuration exists
        When I run gf.config with --show flag
        Then the output should contain "5 x 5"
        And the exit code should be 0
