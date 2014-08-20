from django.conf import settings as default_settings
from django.core.exceptions import ImproperlyConfigured
try:
    from importlib import import_module
except ImportError:  # PY26 # pragma: no cover
    from functools import partial
    import_module = partial(__import__, fromlist=[''])


# DEPRECATED: To be removed in Backends 2.0
import warnings
DID_NOT_HANDLE = object()


class BackendDidNotHandle(Exception):
    """The backend did not perform the expected action"""
    pass


class Proxy(object):
    def __init__(self, possibles, attr):
        self.attr = attr
        self.possibles = possibles

    def __call__(self, *args, **kwargs):
        for possible in self.possibles:
            try:
                ret = getattr(possible, self.attr, None)(*args, **kwargs)
            except BackendDidNotHandle:
                continue
            # DEPRECATED: To be removed in Backends 2.0
            if ret is DID_NOT_HANDLE:
                errmsg = ("DID_NOT_HANDLE is deprecated and will be removed in "
                          "armstrong.utils.backends 2.0. "
                          "Use BackendDidNotHandle.")
                warnings.warn(errmsg, DeprecationWarning, stacklevel=2)
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
