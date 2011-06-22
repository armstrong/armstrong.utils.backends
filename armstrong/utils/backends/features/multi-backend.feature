Feature: MultipleBackendProxy
  In order to allow grouping of multiple backends into one object
  As a developer
  I want to be able to use a proxy object

  Scenario: Single object
    Given I create a MultipleBackendProxy with one backend
    When I call "handle"
    Then I should get the result of from that backend

  Scenario: Multiple objects
    Given I create a MultipleBackendProxy with a null and real backend
    When I call "handle"
    Then I should get the result of the real backend

  Scenario: Attributes return a Proxy object
    Given I create a MultipleBackendProxy with one backend
    When I get a random attribute
    Then I should have a "Proxy" instance

  Scenario: Passing args to call
    Given I create a MultipleBackendProxy with one backend that takes args
    When I call "handle" and pass args
    Then I should get the result of from that backend

  Scenario: Passing kwargs to call
    Given I create a MultipleBackendProxy with one backend that takes kwargs
    When I call "handle" and pass kwargs
    Then I should get the result of from that backend

