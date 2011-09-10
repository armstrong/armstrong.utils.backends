from django.conf import settings as default_settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module


DID_NOT_HANDLE = object()


class Proxy(object):
    def __init__(self, possibles, attr):
        self.attr = attr
        self.possibles = possibles

    def __call__(self, *args, **kwargs):
        for possible in self.possibles:
            ret = getattr(possible, self.attr, None)(*args, **kwargs)
            if ret is DID_NOT_HANDLE:
                continue
            return ret


class MultipleBackendProxy(object):
    def __init__(self, *others):
        self.others = others

    def __getattr__(self, key):
        return Proxy(self.others, key)


class GenericBackend(object):
    proxy_class = MultipleBackendProxy

    def __init__(self, key, settings=None, defaults=None):
        self.key = key
        if not settings:
            settings = default_settings
        self.settings = settings
        self.defaults = defaults

    @property
    def configured_backend(self):
        try:
            return getattr(self.settings, self.key)
        except AttributeError:
            if self.defaults:
                return self.defaults
            msg = "Unable to find '%s' backend, " \
                  "please make sure it is in your settings" % self.key
            raise ImproperlyConfigured(msg)

    def get_backend(self, *args, **kwargs):
        def to_backend(a):
            module, backend_class = a.rsplit(".", 1)
            backend_module = import_module(module)
            return getattr(backend_module, backend_class)

        if type(self.configured_backend) is str:
            return to_backend(self.configured_backend)(*args, **kwargs)
        else:
            return self.proxy_class(*[to_backend(a)(*args, **kwargs) for a in
                self.configured_backend])
