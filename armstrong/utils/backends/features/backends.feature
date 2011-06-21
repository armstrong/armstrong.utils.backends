Feature: Backends
  In order to easily create a new "backend"
  As a developer
  I want to be able to utilize armstrong.utils.backends to handle the heavy lifing

  Scenario: Single backend
    Given I have a single backend configured
    And I create a new backend with the setting used
    When I call "get_backend" on that backend
    Then I should have a copy of the originally configured backend

  Scenario: Multiple backends
    Given I have a list of backends configured
    And I create a new backend with the setting used
    When I call "get_backend" on that backend
    Then I should have a copy of MultipleBackends
