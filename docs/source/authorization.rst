Authorization
=============

To authorize with OK.ru OAuth 2.0 you need :code:`app_id` or :code:`app_key`.
And you need either :code:`session_secret_key` or :code:`app_secret_key`
and :code:`access_token` for executing API requests after authorization.

After authorization you will receive:

* :code:`access_token` aka :code:`session_key`, always
* :code:`session_secret_key` if Implicit Grant / Password Grant used
* :code:`permission_granted` if Implicit Grant used
* :code:`state` if Implicit Grant used
* :code:`token_type` if Code Grant / Refresh Token Grant used
* :code:`refresh_token` if Code Grant used
* :code:`expires_in` if Code Grant / Implicit Grant / Refresh Token Grant used

Authorization Code Grant
------------------------

.. code-block:: python

    from aiookru import CodeSession, API

    app_id = 123456
    app_key = 'abcde'
    app_secret_key = ''

    async with CodeSession(app_id, app_key, app_secret_key, code, redirect_uri) as session:
        api = API(session)
        ...

About OAuth 2.0 Authorization Code Grant: https://oauth.net/2/grant-types/authorization-code/

For more details, see https://apiok.ru/ext/oauth/server

Implicit Grant
--------------

.. code-block:: python

    from aiookru import ImplicitSession, API

    app_id = 123456
    app_key = 'abcde'
    app_secret_key = 'xyz'

    async with ImplicitSession(app_id, app_key, app_secret_key, login, passwd, scope) as session:
        api = API(session)
        ...

About OAuth 2.0 Implicit Grant: https://oauth.net/2/grant-types/implicit/

For more details, see https://apiok.ru/ext/oauth/client

Password Grant
--------------

.. code-block:: python

    from aiookru import PasswordSession, API

    app_id = 123456
    app_key = 'abcde'
    app_secret_key = 'xyz'

    async with PasswordSession(app_id, app_key, app_secret_key, login, passwd) as session:
        api = API(session)
        ...

About OAuth 2.0 Password Grant: https://oauth.net/2/grant-types/password/

Refresh Token
-------------

.. code-block:: python

    from aiookru import RefreshSession, API

    app_id = 123456
    app_key = 'abcde'
    app_secret_key = ''

    async with RefreshSession(app_id, app_key, app_secret_key, refresh_token) as session:
        api = API(session)
        ...

About OAuth 2.0 Refresh Token: https://oauth.net/2/grant-types/refresh-token/

For more details, see https://apiok.ru/ext/oauth/server
