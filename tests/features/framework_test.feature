Feature: BDD Framework Setup Verification
    As a developer
    I want to verify pytest-bdd is correctly configured
    So that BDD tests can be discovered and executed

    Scenario: pytest-bdd framework is working
        Given the pytest-bdd framework is installed
        When I run a simple scenario
        Then the scenario completes successfully
