Session
=======

By default, the sessions try to infer which signature circuit to use:

- if :code:`app_secret_key` and :code:`access_token` are not empty strings - server-server signature circuit is used
- else if :code:`session_secret_key` is not empty string - client-server signature circuit is used
- else exception is raised

You can explicitly choose a circuit for signing requests
by passing to :code:`API` one of the following sessions:

Client-Server signature circuit
-------------------------------

ClientSession
~~~~~~~~~~~~~

:code:`ClientSession` is a subclass of :code:`TokenSession`.

.. code-block:: python

    from aiookru import ClientSession, API

    session = ClientSession(app_id, 'app key', 'session secret key')
    api = API(session)
    ...

CodeClientSession
~~~~~~~~~~~~~~~~~

:code:`CodeClientSession` is a subclass of :code:`CodeSession`.

.. code-block:: python

    from aiookru import CodeClientSession, API

    async with CodeClientSession(app_id, 'app key', code, redirect_uri) as session:
        api = API(session)
        ...

ImplicitClientSession
~~~~~~~~~~~~~~~~~~~~~

:code:`ImplicitClientSession` is a subclass of :code:`ImplicitSession`.

.. code-block:: python

    from aiookru import ImplicitClientSession, API

    async with ImplicitClientSession(app_id, 'app key', login, passwd, scope) as session:
        api = API(session)
        ...

PasswordClientSession
~~~~~~~~~~~~~~~~~~~~~

:code:`PasswordClientSession` is a subclass of :code:`PasswordSession`.

.. code-block:: python

    from aiookru import PasswordClientSession, API

    async with PasswordClientSession(app_id, 'app key', login, passwd) as session:
        api = API(session)
        ...

RefreshClientSession
~~~~~~~~~~~~~~~~~~~~

:code:`RefreshClientSession` is a subclass of :code:`RefreshSession`.

.. code-block:: python

    from aiookru import RefreshClientSession, API

    async with RefreshClientSession(app_id, 'app key', refresh_token) as session:
        api = API(session)
        ...

Server-Server signature circuit
-------------------------------

ServerSession
~~~~~~~~~~~~~

:code:`ServerSession` is a subclass of :code:`TokenSession`.

.. code-block:: python

    from aiookru import ServerSession, API

    session = ServerSession(app_id, 'app key', 'app secret key', 'access token')
    api = API(session)
    ...

CodeServerSession
~~~~~~~~~~~~~~~~~

:code:`CodeServerSession` is a subclass of :code:`CodeSession`.

.. code-block:: python

    from aiookru import CodeServerSession, API

    async with CodeServerSession(app_id, 'app key', 'app secret key', code, redirect_uri) as session:
        api = API(session)
        ...

ImplicitServerSession
~~~~~~~~~~~~~~~~~~~~~

:code:`ImplicitServerSession` is a subclass of :code:`ImplicitSession`.

.. code-block:: python

    from aiookru import ImplicitServerSession, API

    async with ImplicitServerSession(app_id, 'app key', 'app secret key', login, passwd, scope) as session:
        api = API(session)
        ...

PasswordServerSession
~~~~~~~~~~~~~~~~~~~~~

:code:`PasswordServerSession` is a subclass of :code:`PasswordSession`.

.. code-block:: python

    from aiookru import PasswordServerSession, API

    async with PasswordServerSession(app_id, 'app key', 'app secret key', login, passwd scope) as session:
        api = API(session)
        ...

RefreshServerSession
~~~~~~~~~~~~~~~~~~~~

:code:`RefreshServerSession` is a subclass of :code:`RefreshSession`.

.. code-block:: python

    from aiookru import RefreshServerSession, API

    async with RefreshServerSession(app_id, 'app key', 'app secret key', refresh_token) as session:
        api = API(session)
        ...
