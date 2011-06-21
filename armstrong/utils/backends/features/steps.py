# -*- coding: utf-8 -*-
from lettuce import *

from armstrong.utils.backends.base import GenericBackend, MultipleBackendProxy
from django.conf import settings
import fudge


@before.each_scenario
def setup_scenario(scenario):
    world.backend = None
    world.exception = None
    world.result = None
    world.attr = None
    world.backend_name = "%s.simple_backend" % simple_backend.__module__


def null_backend(*args, **kwargs):
    pass


def simple_backend(*args, **kwargs):
    return simple_backend.message
simple_backend.message = "I'm a simple backend"


def second_backend(*args, **kwargs):
    return second_backend.message
second_backend.message = "I am the second backend"


@step(u'I have a single backend configured')
def configure_single_backend(step):
    assert False, 'This step must be implemented'


@step(u'I have a string configured for the backend')
def given_i_have_a_string_configured_for_the_backend(step):
    world.backend_name = "%s.simple_backend" % simple_backend.__module__
    world.expected_backend = simple_backend
    settings.testable_backends = world.backend_name


@step(u'I have a list configured for the backend')
def configure_list_of_backends(step):
    world.backend_name = ["%s.simple_backend" % simple_backend.__module__,
                          "%s.second_backend" % second_backend.__module__, ]
    settings.testable_backends = world.backend_name


@step(u'I create a new backend with the setting used')
def create_backend(step):
    assert False, 'This step must be implemented'


@step(u'I call "(.*)" on that backend')
def backend_call(step, method):
    assert hasattr(world.backend, method)
    try:
        world.result = getattr(world.backend, method)()
    except Exception, e:
        world.exception = e


@step(u'I should have a copy of the originally configured backend')
def expect_single_backend(step):
    assert False, 'This step must be implemented'


@step(u'I should have a copy of MultipleBackends')
def expect_multiple_backends(step):
    assert False, 'This step must be implemented'



@step(u'I instantiate a new GenericBackend$')
def create_backend_with_string(step):
    world.backend = GenericBackend("testable_backends")


@step(u'I instantiate a new GenericBackend with an unknown key$')
def create_backend_with_unknown_key(step):
    world.backend = GenericBackend("unknown_and_unknowable")


@step(u'I have new GenericBackend object instantiated with a list')
def create_backend_with_list(step):
    assert False, 'This step must be implemented'


@step(u'I should get that function back as the result')
def expect_function(step):
    assert world.result == world.expected_backend, \
            "Failed: %s == %s" % (world.result, world.expected_backend)


@step(u'I create a new GenericBackend object with a settings kwarg')
def create_backend_with_settings(step):
    settings = fudge.Fake()
    settings.has_attr(testable_backends = "%s.second_backend" % \
            second_backend.__module__)

    world.backend = GenericBackend("testable_backends", settings=settings)


@step(u'I create a new GenericBackend object without a settings kwarg')
def create_backend_without_settings(step):
    world.backend = GenericBackend("testable_backends")


@step(u'it should pay attention to the configured settings')
def expect_configured_settings(step):
    assert world.attr == "%s.second_backend" % second_backend.__module__
    assert world.attr != "%s.simple_backend" % simple_backend.__module__


@step(u'it should pay attention to the global settings')
def expect_global_settings(step):
    assert world.attr != "%s.second_backend" % second_backend.__module__
    assert world.attr == "%s.simple_backend" % simple_backend.__module__


@step(u'I get the "(.*)" attribute')
def fetch_attribute(step, attr):
    assert hasattr(world.backend, attr)
    world.attr = getattr(world.backend, attr)


@step(u'it should be the same as the initial value passed to __init__')
def check_attr_for_original(step):
    assert world.attr == world.backend_name


@step(u'I should get a MultipleBackendProxy object back')
def expect_multi_backend_proxy_backend(step):
    assert isinstance(world.result, MultipleBackendProxy)


@step(u'I expect to have an "(.*)" exception thrown')
def catch_exception(step, exception_name):
    assert world.exception is not None
    assert world.exception.__class__.__name__ == exception_name, "%s != %s" % (
            world.exception.__class__.__name__, exception_name)

@step(u'And have the message: "(.*)"')
def exception_message(step, message):
    assert world.exception.message == message, "%s != %s" % (
            world.exception.message, message)
