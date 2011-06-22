from django.conf import settings as default_settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module


class Proxy(object):
    def __init__(self, attr):
        self.attr = attr

    def __call__(self, **kwargs):
        return self.attr(**kwargs)

class MultipleBackendProxy(object):
    def __init__(self, *others):
        self.others = others

    def __getattr__(self, key):
        return Proxy(self.others[0])


class GenericBackend(object):
    def __init__(self, key, settings=None):
        self.key = key
        if not settings:
            settings = default_settings
        self.settings = settings

    @property
    def configured_backend(self):
        try:
            return getattr(self.settings, self.key)
        except AttributeError:
            msg = "Unable to find '%s' backend, " \
                  "please make sure it is in your settings" % self.key
            raise ImproperlyConfigured(msg)

    def get_backend(self):
        def to_backend(a):
            module, backend_class = a.rsplit(".", 1)
            backend_module = import_module(module)
            return getattr(backend_module, backend_class)

        if type(self.configured_backend) is str:
            return to_backend(self.configured_backend)
        else:
            return MultipleBackendProxy(*[to_backend(a) for a in
                self.configured_backend])
