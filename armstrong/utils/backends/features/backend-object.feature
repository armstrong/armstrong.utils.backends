Feature: GenericBackend
  In order to have programmatic access to a generic backend
  As a developer
  I want to be able to interact with a GenericBackend instance

  Scenario: configured_backend
    Given I have a string configured for the backend
    And I instantiate a new GenericBackend
    When I get the "configured_backend" attribute
    Then it should be the same as the initial value passed to __init__

  Scenario: get_backend
    Given I have a string configured for the backend
    And I instantiate a new GenericBackend
    When I call "get_backend" on that backend
    Then I should get an instantiated object back as the result

  Scenario: get_backend with multiple backends
    Given I have a list configured for the backend
    And I instantiate a new GenericBackend
    When I call "get_backend" on that backend
    Then I should get a MultipleBackendProxy object back

  Scenario: Passing args to get_backend
    Given I have a string configured for the backend
    And I instantiate a new GenericBackend
    When I call "get_backend" with args on the backend
    Then I should get an instantiated object back as the result
    And its arguments should match what was provided

  Scenario: Passing kwargs to get_backend
    Given I have a string configured for the backend
    And I instantiate a new GenericBackend
    When I call "get_backend" with kwargs on the backend
    Then I should get an instantiated object back as the result
    And its arguments should match what was provided

  Scenario: Injecting settings
    Given I have a string configured for the backend
    And I create a new GenericBackend object with a settings kwarg
    When I get the "configured_backend" attribute
    Then it should pay attention to the configured settings

  Scenario: Default settings
    Given I have a string configured for the backend
    And I create a new GenericBackend object without a settings kwarg
    When I get the "configured_backend" attribute
    Then it should pay attention to the global settings

  Scenario: Unable to find settings
    Given I instantiate a new GenericBackend with an unknown key
    When I call "get_backend" on that backend
    Then I expect to have an "ImproperlyConfigured" exception thrown
    And have the message: "Unable to find 'unknown_and_unknowable' backend, please make sure it is in your settings"

  Scenario: Default backends
    Given I instantiate a new GenericBackend with an unknown key and defaults
    When I call "get_backend" on that backend
    Then I should get that function back as the result
