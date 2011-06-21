# -*- coding: utf-8 -*-
from lettuce import step

from armstrong.utils.backends.base import GenericBackend


@step(u'I have a single backend configured')
def configure_single_backend(step):
    assert False, 'This step must be implemented'


@step(u'I have a list of backends configured')
def configure_list_of_backends(step):
    assert False, 'This step must be implemented'


@step(u'I create a new backend with the setting used')
def create_backend(step):
    assert False, 'This step must be implemented'


@step(u'I call "(.*)" on that backend')
def backend_call(step, method):
    assert False, 'This step must be implemented'


@step(u'I should have a copy of the originally configured backend')
def expect_single_backend(step):
    assert False, 'This step must be implemented'


@step(u'I should have a copy of MultipleBackends')
def expect_multiple_backends(step):
    assert False, 'This step must be implemented'


@step(u'Given I have new GenericBackend object')
def given_i_have_new_genericbackend_object(step):
    assert False, 'This step must be implemented'


@step(u'call "(.*)" on that object')
def execute_function(step, func):
    assert False, 'This step must be implemented'


@step(u'I should get that function back as the result')
def expect_function(step):
    assert False, 'This step must be implemented'


@step(u'I access the "(.*)" property')
def access_property(step, attr):
    assert False, 'This step must be implemented'


@step(u'I create a new GenericBackend object with a settings kwarg')
def create_backend_with_settings(step):
    assert False, 'This step must be implemented'


@step(u'I create a new GenericBackend object without a settings kwarg')
def create_backend_without_settings(step):
    assert False, 'This step must be implemented'


@step(u'it should pay attention to the configured settings')
def expect_configured_settings(step):
    assert False, 'This step must be implemented'


@step(u'it should pay attention to the global settings')
def expect_global_settings(step):
    assert False, 'This step must be implemented'


@step(u'When I get the "(.*)" attribute')
def when_i_get_the_group1_attribute(step, group1):
    assert False, 'This step must be implemented'
@step(u'Then it should be the same as the initial value passed to __init__')
def then_it_should_be_the_same_as_the_initial_value_passed_to___init__(step):
    assert False, 'This step must be implemented'
@step(u'Then I should get a MultipleBackendProxy object back')
def then_i_should_get_a_multiplebackendproxy_object_back(step):
    assert False, 'This step must be implemented'

