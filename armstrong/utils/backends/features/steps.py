# -*- coding: utf-8 -*-
from lettuce import *

from armstrong.utils.backends.base import GenericBackend, MultipleBackendProxy
from armstrong.utils.backends import base
from django.conf import settings
import fudge
import random


@before.each_scenario
def setup_scenario(scenario):
    world.backend = None
    world.exception = None
    world.result = None
    world.attr = None
    world.proxy = None
    world.expected_return = None
    world.provided_args = None
    world.provided_kwargs = None
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


@step(u'I create a MultipleBackendProxy with one backend$')
def create_simple_proxy(step):
    world.expected_return = "some random value %d" % random.randint(100, 200)
    fake = fudge.Fake(callable=True).returns(world.expected_return)
    world.proxy = MultipleBackendProxy(fake)


@step(u'I create a MultipleBackendProxy with one backend that takes args$')
def create_proxy_with_args(step):
    world.provided_args = {
            "msg": "Hello world",
            "random": random.randint(100, 200),
    }
    fake = fudge.Fake(callable=True) \
            .with_args(**world.provided_args) \
            .returns(world.provided_args)
    world.proxy = MultipleBackendProxy(fake)
    world.expected_return = world.provided_args


@step(u'I create a MultipleBackendProxy with one backend that takes kwargs$')
def create_proxy_with_kwargs(step):
    world.provided_kwargs = {
            "msg": "Hello world",
            "random": random.randint(100, 200),
    }
    fake = fudge.Fake(callable=True) \
            .with_args(**world.provided_kwargs) \
            .returns(world.provided_kwargs)
    world.proxy = MultipleBackendProxy(fake)
    world.expected_return = world.provided_kwargs


@step(u'I get a random attribute')
def random_attr(step):
    attr = "random_%d" % random.randint(10000, 20000)
    world.attr = getattr(world.proxy, attr)


@step(u'I should have a "(.*)" instance')
def instance_check(step, class_name):
    instance = getattr(base, class_name)

    assert isinstance(world.attr, instance), "%s is not an instance of %s" % (
            world.attr, instance)


@step(u'When I call "(.*)"$')
def when_i_call_group1(step, func):
    world.attr = getattr(world.proxy, func)
    world.result = world.attr()


@step(u'I should get the result of from that backend')
def check_proxied_return(step):
    assert world.expected_return == world.result, \
            '"%s" is not equal to "%s"' % (world.expected_return, world.result)


@step(u'I call "(.*)" and pass args')
def call_with_args(step, func):
    world.attr = getattr(world.proxy, func)
    world.result = world.attr(**world.provided_args)


@step(u'I call "(.*)" and pass kwargs')
def call_with_kwargs(step, func):
    world.attr = getattr(world.proxy, func)
    world.result = world.attr(**world.provided_kwargs)
