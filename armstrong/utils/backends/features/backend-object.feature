Feature: GenericBackend
  In order to have programmatic access to a generic backend
  As a developer
  I want to be able to interact with a GenericBackend instance

  Scenario: configured_backend
    Given I have new GenericBackend object instantiated with a string
    When I get the "configured_backend" attribute
    Then it should be the same as the initial value passed to __init__

  Scenario: get_backend
    Given I have new GenericBackend object instantiated with a string
    When I call "get_backend" on that object
    Then I should get that function back as the result

  Scenario: get_backend with multiple backends
    Given I have new GenericBackend object instantiated with a list
    When I call "get_backend" on that object
    Then I should get a MultipleBackendProxy object back

  Scenario: Injecting settings
    Given I create a new GenericBackend object with a settings kwarg
    When I access the "configured_backend" property
    Then it should pay attention to the configured settings

  Scenario: Default settings
    Given I create a new GenericBackend object without a settings kwarg
    When I access the "configured_backend" property
    Then it should pay attention to the global settings
