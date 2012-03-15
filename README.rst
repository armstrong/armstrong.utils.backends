armstrong.utils.backends
========================
Generic backend system to use throughout Armstrong


Usage
-----
You can use this to handle loading one or more "backends" that need to be
configured at runtime.  To create a new ``backend`` object, you would do
something like this in your ``__init__.py``::

    backends = GenericBackend("MY_BACKEND_KEY")

``MY_BACKEND_KEY`` is the name of the key that the end user sets in their
``settings.py`` file.  The end-user should set it to either a string or a list.

You can also provide a default backend (or backends) by setting the
``defaults`` kwarg for ``GenericBackend``::

    default_backends = ["myapp.backends.TwitterBackend",
                        "myapp.backends.FacebookBackend", ]
    backends = GenericBackend("MY_BACKEND_KEY", defaults=default_backends)

When you're ready to use the backends, you can call ``get_backend`` to retrieve
the backend to use.  This is done after instantiation to allow for the value to
change depending on the context that it was called in.


Writing Backends
""""""""""""""""
Backends are simple objects that do any particular task.  Beyond using
``get_backend`` to handle the creation of the backend, you treat it as if you
were calling it directly.

All attributes (and methods) accessed on the backend are proxied to handle
dispatching to multiple backends.

All backends should return something.  If they were unable to process the
response they should return ``armstrong.utils.backends.DID_NOT_HANDLE``


Installation
------------

Use `pip`_ to install like this::

    pip install armstrong.utils.backends

.. _pip: http://www.pip-installer.org/

Contributing
------------

* Create something awesome -- make the code better, add some functionality,
  whatever (this is the hardest part).
* `Fork it`_
* Create a topic branch to house your changes
* Get all of your commits in the new topic branch
* Submit a `pull request`_

.. _Fork it: http://help.github.com/forking/
.. _pull request: http://help.github.com/pull-requests/


State of Project
----------------
Armstrong is an open-source news platform that is freely available to any
organization.  It is the result of a collaboration between the `Texas Tribune`_
and `Bay Citizen`_, and a grant from the `John S. and James L. Knight
Foundation`_.

To follow development, be sure to join the `Google Group`_.

``armstrong.utils.backends`` is part of the `Armstrong`_ project.  You're
probably looking for that.

.. _Texas Tribune: http://www.texastribune.org/
.. _Bay Citizen: http://www.baycitizen.org/
.. _John S. and James L. Knight Foundation: http://www.knightfoundation.org/
.. _Google Group: http://groups.google.com/group/armstrongcms
.. _Armstrong: http://www.armstrongcms.org/


License
-------
Copyright 2011-2012 Bay Citizen and Texas Tribune

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
