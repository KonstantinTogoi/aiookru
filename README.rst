.. image:: https://img.shields.io/badge/license-BSD-blue.svg
    :target: https://github.com/KonstantinTogoi/aiookru/blob/master/LICENSE

.. image:: https://img.shields.io/pypi/v/aiookru.svg
    :target: https://pypi.python.org/pypi/aiookru

.. image:: https://img.shields.io/pypi/pyversions/aiookru.svg
    :target: https://pypi.python.org/pypi/aiookru

.. image:: https://readthedocs.org/projects/aiookru/badge/?version=latest
    :target: https://aiookru.readthedocs.io/en/latest/

.. image:: https://travis-ci.org/KonstantinTogoi/aiookru.svg
    :target: https://travis-ci.org/KonstantinTogoi/aiookru

.. index-start-marker1

aiookru
=======

aiookru is a python `ok.ru API <https://apiok.ru/>`_ wrapper.
The main features are:

* authorization (`Authorization Code <https://oauth.net/2/grant-types/authorization-code/>`_, `Implicit Flow <https://oauth.net/2/grant-types/implicit/>`_, `Password Grant <https://oauth.net/2/grant-types/password/>`_, `Refresh Token <https://oauth.net/2/grant-types/refresh-token/>`_)
* `REST API <https://apiok.ru/en/dev/methods/rest>`_ methods


Usage
-----

To use `ok.ru API <https://apiok.ru/>`_ you need a registered app
and `ok.ru <https://ok.ru>`_ account.
For more details, see
`aiookru Documentation <https://aiookru.readthedocs.io/>`_.

Client application
~~~~~~~~~~~~~~~~~~

Use :code:`ClientSession` when REST API is needed in:

- client component of the client-server application
- standalone mobile/desktop application

i.e. when you embed your app's info (application key) in publicly available code.

.. code-block:: python

    from aiookru import ClientSession, API

    session = ClientSession(app_id, app_key, access_token, session_secret_key)
    api = API(session)

    events = await api.events.get()
    friends = await api.friends.get()

Pass :code:`session_secret_key` and :code:`access_token`
that were received after authorization.
For more details, see
`authorization instruction <https://aiookru.readthedocs.io/en/latest/authorization.html>`_.

Server application
~~~~~~~~~~~~~~~~~~

Use :code:`ServerSession` when REST API is needed in:

- server component of the client-server application
- requests from your servers

.. code-block:: python

    from aiookru import ServerSession, API

    session = ServerSession(app_id, app_key, app_secret_key, access_token)
    api = API(session)

    events = await api.events.get()
    friends = await api.friends.get()

Pass :code:`app_secret_key` and :code:`access_token` that was received after authorization.
For more details, see
`authorization instruction <https://aiookru.readthedocs.io/en/latest/authorization.html>`_.

Installation
------------

.. code-block:: shell

    pip install aiookru

or

.. code-block::

    python setup.py install

Supported Python Versions
-------------------------

Python 3.5, 3.6, 3.7 and 3.8 are supported.

.. index-end-marker1

Test
----

Run all tests.

.. code-block:: shell

    python setup.py test

Run tests with PyTest.

.. code-block:: shell

    python -m pytest [-k TEST_NAME]

License
-------

**aiookru** is released under the BSD 2-Clause License.
