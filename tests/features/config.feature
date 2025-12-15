Feature: Printer Configuration
    As a user
    I want to configure my printer bed dimensions
    So that drawer-fit calculations account for my printer's limits

    Scenario: Initialize config with --init flag
        Given no printer configuration exists
        When I run gf.config with --init flag providing dimensions
        Then the exit code should be 0
        And the output should contain "saved"

    Scenario: Display config with --show flag
        Given a printer configuration exists
        When I run gf.config with --show flag
        Then the exit code should be 0
        And the output should contain "mm"

    Scenario: Error when no flags provided
        Given a printer configuration exists
        When I run gf.config without flags
        Then the exit code should be 1
        And the output should contain "Error"

    Scenario: Max gridfinity units calculated correctly
        Given a printer configuration exists
        When I run gf.config with --show flag
        Then the output should contain "Max gridfinity units"
        And the exit code should be 0
