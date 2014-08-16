import fudge
import warnings
from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured

from armstrong.dev.tests.utils.base import ArmstrongTestCase
from armstrong.utils.backends.base import (
    Proxy, MultipleBackendProxy, GenericBackend, BackendDidNotHandle,
    DID_NOT_HANDLE)
from .support.backends import UseThisOne


class ProxyTestCase(ArmstrongTestCase):
    def test_empty_proxy(self):
        p = Proxy([], 'func')
        self.assertIsNone(p())

    @fudge.test
    def test_calls_attr_on_possible(self):
        obj = fudge.Fake().expects('func')
        p = Proxy([obj], 'func')
        p()

    @fudge.test
    def test_calls_attr_with_args_and_kwargs(self):
        obj = fudge.Fake().expects('func').with_args('arg1', 'arg2', kw=1)
        p = Proxy([obj], 'func')
        p('arg1', 'arg2', kw=1)

    @fudge.test
    def test_only_uses_first_possibility_that_works(self):
        obj1 = fudge.Fake().expects('func').with_args('arg1', kw=1).returns(1)
        obj2 = fudge.Fake().provides('func').returns(2)
        p = Proxy([obj1, obj2], 'func')
        self.assertEqual(p('arg1', kw=1), 1)

    @fudge.test
    def test_skips_backenddidnothandle(self):
        obj1 = fudge.Fake().expects('func').raises(BackendDidNotHandle)
        obj2 = fudge.Fake().expects('func').with_args('arg1', kw=1)
        p = Proxy([obj1, obj2], 'func')
        p('arg1', kw=1)

    # DEPRECATED: To be removed in Backends 2.0
    @fudge.test
    def test_skips_did_not_handle(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            obj1 = fudge.Fake().expects('func').returns(DID_NOT_HANDLE)
            obj2 = fudge.Fake().expects('func').with_args('arg1', kw=1)
            p = Proxy([obj1, obj2], 'func')
            p('arg1', kw=1)

    @fudge.test
    def test_returns_expected_value(self):
        obj = fudge.Fake().expects('func').returns("proxy returned me")
        p = Proxy([obj], 'func')
        self.assertEqual(p(), "proxy returned me")


class MultipleBackendProxyTestCase(ArmstrongTestCase):
    @fudge.test
    def test_wraps_multiple_things_in_proxy(self):
        obj1 = fudge.Fake().expects('func').raises(BackendDidNotHandle)
        obj2 = fudge.Fake().provides('func').returns(2)
        m = MultipleBackendProxy(obj1, obj2)
        self.assertEqual(m.func(), 2)

    # DEPRECATED: To be removed in Backends 2.0
    @fudge.test
    def test_wraps_multiple_things_in_proxy_deprecated(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            obj1 = fudge.Fake().expects('func').returns(DID_NOT_HANDLE)
            obj2 = fudge.Fake().provides('func').returns(2)
            m = MultipleBackendProxy(obj1, obj2)
            self.assertEqual(m.func(), 2)


class GenericBackendTestCase(ArmstrongTestCase):
    def test_use_django_settings_by_default(self):
        b = GenericBackend('cfg')
        self.assertEqual(b.settings, django_settings)

    def test_looks_for_key_in_django_settings(self):
        b = GenericBackend('cfg')
        with self.settings(cfg='cfg_value'):
            self.assertEqual(django_settings.cfg, 'cfg_value')
            self.assertEqual(b.configured_backend, 'cfg_value')

    @fudge.test
    def test_use_provided_settings_instead_of_django(self):
        my_settings = fudge.Fake().has_attr(cfg='my value')
        b = GenericBackend('cfg', settings=my_settings)
        with self.settings(cfg='django value'):
            self.assertEqual(b.configured_backend, 'my value')

    def test_uses_provided_default_if_key_not_in_settings(self):
        b = GenericBackend('cfg', defaults='other cfg')
        self.assertEqual(b.configured_backend, 'other cfg')

    def test_raises_improperly_configured_if_no_key_and_no_default(self):
        with self.assertRaises(ImproperlyConfigured):
            GenericBackend('cfg').configured_backend

    def test_get_backend_returns_instance_of_cls(self):
        b = GenericBackend('key', defaults='tests.support.backends.UseThisOne')
        obj = b.get_backend()
        self.assertIsInstance(obj, UseThisOne)

    @fudge.test
    def test_get_backend_inits_resulting_cls(self):
        b = GenericBackend('key', defaults='tests.support.backends.TestArgs')
        b.get_backend('arg1', kw=1)

    @fudge.test
    def test_get_backend_returns_instance_with_expected_method(self):
        b = GenericBackend('cfg', defaults='tests.support.backends.UseThisOne')
        result = b.get_backend().func('arg1', kw=1)
        self.assertEqual(result, "backend returned me")

    @fudge.test
    def test_configured_backend_can_be_iterable(self):
        backends = [
            'tests.support.backends.Skip',
            'tests.support.backends.UseThisOne']
        with self.settings(cfg=backends):
            b = GenericBackend('cfg').get_backend()
            result = b.func('arg1', kw=1)
            self.assertEqual(result, "backend returned me")
