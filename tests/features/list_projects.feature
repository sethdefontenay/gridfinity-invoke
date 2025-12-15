Feature: List Projects
    As a user
    I want to list all my Gridfinity projects
    So that I can see what projects I have

    Scenario: Display all projects with active indicator
        Given multiple projects exist
        When I list all projects
        Then the output should contain project names
        And the active project should be marked
        And the exit code should be 0

    Scenario: Empty state shows no projects message
        Given no projects exist
        When I list all projects
        Then the output should contain "No projects found"
        And the exit code should be 0
