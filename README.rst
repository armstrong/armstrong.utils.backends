armstrong.utils.backends
========================

.. image:: https://travis-ci.org/armstrong/armstrong.utils.backends.svg?branch=master
  :target: https://travis-ci.org/armstrong/armstrong.utils.backends
  :alt: TravisCI status
.. image:: https://img.shields.io/coveralls/armstrong/armstrong.utils.backends.svg
  :target: https://coveralls.io/r/armstrong/armstrong.utils.backends
  :alt: Coverage status
.. image:: https://img.shields.io/pypi/v/armstrong.utils.backends.svg
  :target: https://pypi.python.org/pypi/armstrong.utils.backends/
  :alt: PyPI Version
.. image:: https://img.shields.io/pypi/l/armstrong.utils.backends.svg
  :target: https://pypi.python.org/pypi/armstrong.utils.backends/
  :alt: License

Generic backend system to use throughout Armstrong


Usage
-----
Dynamically load a Python module at runtime and use it as if you'd hardcoded
the module directly. This allows flexibility. It's polymorphism in action.

Why? In the Armstrong internals we do a bunch of stuff via backends. If you
want to do that stuff differently, make a class with the same interface and
provide your class as the backend. Armstrong will work *its* magic the way
*you* want. In many cases, Armstrong ships with support for multiple common
scenarios (implemented as backends) and you can pick the one that fits your
needs.

Following the Django paradigm, create a ``key = value`` in ``setttings.py``
where the value is a string or a list of strings of full, dotted, Python
import paths. That module will be imported at runtime and used *exactly*
as if you had instantiated it directly. An example::

    # hello/world.py
    class Hello(object):
        def hi(self):
            print("Hello world!")

    # hello/armstrong.py
    class Hello(object):
        def hi(self):
            print("Hello Armstrong!")

    # settings.py  <-- armstrong.utils.backends uses Django settings by default
    HELLO_CLASS = "hello.armstrong.Hello"

    # somewhere_else.py or in a console
    >>> from armstrong.utils.backends import GenericBackend
    >>> hello = GenericBackend("HELLO_CLASS").get_backend()
    >>> hello.hi()
    Hello Armstrong!

A **default** can be provided and the process works like the standard Python
dict.get() where if the key doesn't exist in the settings, there's a fallback.
(This is how Armstrong specifies its defaults so you aren't required to change
your settings.py if satisfied with the default behavior.)::

    >>> backend = GenericBackend("MISSING_KEY", defaults="hello.world.Hello")
    >>> hello = backend.get_backend()
    >>> hello.hi()
    Hello world!

Calling ``get_backend()`` is the equivalent of instantiation. So whenever
you're ready to use the dynamically loaded class, call ``get_backend``.
Pass in any parameters you'd normally use. Think of it as ``__init__``.
These are the same::

   GenericBackend("HELLO_CLASS").get_backend(1, two=2)
   Hello(1, two=2)

You can pass in a **different settings** module with the ``settings`` kwarg if you
want the backend loader to look somewhere other than Django settings.

Multiple backends
"""""""""""""""""
Another powerful feature? Feeding in multiple possible backends. Armstrong
will perform the action you want by going down the list of backends stopping
at the first one that does its job. If the backend's method raises a
``BackendDidNotHandle`` exception, Armstrong will try the next backend.
A pseudo code example::

    default_backends = ["myapp.backends.TwitterBackend",
                        "myapp.backends.FacebookBackend"]
    backend = GenericBackend("SOCIAL_NETWORKS", defaults=default_backends)

    # myapp.backends.py
    class TwitterBackend(object):
        def post(msg):
            if not self.user.has_account:
                raise BackendDidNotHandle("No account for that user")

    social_network = backend.get_backend(user)
    social_network.post("Armstrong is pretty sweet you guys")


Writing Backends
""""""""""""""""
Backends are classes. ``GenericBackend`` is a way to dynamically load those
classes. Beyond using ``get_backend`` to handle the creation of the backend,
you treat it as if you were calling it directly.

If you are using multiple backends, all attributes (and methods) accessed on
the backend are proxied to handle the dispatching. To have a backend abdicate
and have the loader use the next backend in the list, have the backend
method raise ``armstrong.utils.backends.BackendDidNotHandle``.


Installation & Configuration
----------------------------
Supports Django 1.3, 1.4, 1.5, 1.6, 1.7 on Python 2.6 and 2.7.

#. ``pip install armstrong.utils.backends``


Contributing
------------
Development occurs on Github. Participation is welcome!

* Found a bug? File it on `Github Issues`_. Include as much detail as you
  can and make sure to list the specific component since we use a centralized,
  project-wide issue tracker.
* Testing? ``pip install tox`` and run ``tox``
* Have code to submit? Fork the repo, consolidate your changes on a topic
  branch and create a `pull request`_. The `armstrong.dev`_ package provides
  tools for testing, coverage and South migration as well as making it very
  easy to run a full Django environment with this component's settings.
* Questions, need help, discussion? Use our `Google Group`_ mailing list.

.. _Github Issues: https://github.com/armstrong/armstrong/issues
.. _pull request: http://help.github.com/pull-requests/
.. _armstrong.dev: https://github.com/armstrong/armstrong.dev
.. _Google Group: http://groups.google.com/group/armstrongcms


State of Project
----------------
`Armstrong`_ is an open-source news platform that is freely available to any
organization. It is the result of a collaboration between the `Texas Tribune`_
and `Bay Citizen`_ and a grant from the `John S. and James L. Knight
Foundation`_. Armstrong is available as a complete bundle and as individual,
stand-alone components.

.. _Armstrong: http://www.armstrongcms.org/
.. _Bay Citizen: http://www.baycitizen.org/
.. _Texas Tribune: http://www.texastribune.org/
.. _John S. and James L. Knight Foundation: http://www.knightfoundation.org/
