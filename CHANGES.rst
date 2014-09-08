CHANGES
=======

1.1.1 (2014-09-07)
------------------

- Fix relative imports in Python 2.6. All Djangos supporting 2.6 provide
  ``import_module``, which is more reliable than ``__import__``.


1.1.0 (2014-09-05)
------------------

- **DEPRECATION:** deprecate DID_NOT_HANDLE. Raising a ``BackendDidNotHandle``
  exception is now the preferred way to skip when using multiple backends.

- Support for Django 1.7 (removes a deprecation warning)

- Expanded documentation with examples

- Use Setuptools and pkg_resources for namespacing

- Development: use ArmDev 2.0
