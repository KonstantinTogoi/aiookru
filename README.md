# ok.ru Python REST API wrapper

- [About](#about)
- [Getting Started](#getting-started)
    + [ImplicitSession](#implicitsession)
    + [TokenSession](#tokensession)
    + [Executing API requests](#executing-api-requests)
        - [Client-Server signature circuit](#client-server-circuit)
        - [Server-Server signature circuit](#sever-server-circuit)
- [License](#license)


## About

This is [ok.ru](https://ok.ru) (Russian social network) python API wrapper.
The goal is to support all API methods: https://apiok.ru/en/dev/methods/rest.


## Getting Started

Install package using pip

```bash
pip install aiookru
```

To use OK API you need a registered app and login in the social network.

1. Sign up in [ok.ru](https://ok.ru)
2. Create **external** application.
3. Save **App ID**, **App key**, **App secret key**.
4. Use App ID, list of required permissions and user credentials to get **access token**.
5. Use the access token to make method requests.

After signing up got to https://apiok.ru/en/dev/app/create and create application.

```python
app_id = 'app ID'
app_key = 'app key'
app_secret_key = 'app secret'
```

### ImplicitSession

You can authenticate with [OK API OAuth](https://apiok.ru/en/ext/oauth/) by passing user credentials and permissions to `ImplicitSession` (or `ImplicitClientSession`/
`ImplicitServerSession`).

```python
from aiookru import ImplicitSession

phone = '+1999123456'
password = 'user password'

session = await ImplicitSession(
    app_id=app_id,
    app_key=app_key,
    app_secret_key=app_secret_key,
    login=phone,
    passwd=password,
    permissions='VALUABLE_ACCESS',
)
```

Now you can execute API requests (see [Executing API requests](#executing-api-requests)).
After authentication you will get access token **session.access_token** and
session secret key **session.session_secret_key**. Save them to make requests later:

```python
access_token = session.access_token
session_secret_key = session.session_secret_key
```

### TokenSession

If you already have either of two:

- `app_secret_key` and `access_token`
- `session_secret_key`

```python
from aiookru import TokenSession

session = TokenSession(
    app_key=app_key,
    app_secret_key=app_secret_key,
    access_token=access_token,
    session_secret_key=session_secret_key,
)
```

you can instantiate `TokenSession` (or `ClinentSession`/`ServerSession`) and execute requests.


### Executing API requests

```python
from aiookru import API

api = API(session)

# current user's friends
friends = await api.friends.get()
```

Under the hood each API requests is encriched with:

- `application_key`
- `sig`
- `app_secret_key` and `access_token` or `session_secret_key` 
- `format`
- `method`

By default, the sessions try to infer which signature circuit to use:

- if `app_secret_key` and `access_token` are not empty strings - server-server signature circuit is used
- else if `session_secret_key` is not empty string - client-server signature circuit is used
- else exception is raised

You can explicitly choose a circuit for signing requests by passing to `API` one
of the following sessions:

#### Sever-Server circuit

```python
from aiookru import ImplicitServerSession, API
session = await ImplicitServerSession(app_id, app_key, app_secret_key, phone, password)
api = API(session)
```

or if you already have an access token

```python
from aiookru import ServerSession, API
session = ServerSession(app_key, app_secret_key, access_token)
```

#### Client-Server circuit

```python
from aiookru import ImplicitClientSession, API
session = await ImplicitClientSession(app_id, app_key, phone, password)
api = API(session)
```

or if you already have a session secret key

```python
from aiookru import ClientSession, API
session = await ClientSession(app_key, session_secret_key)
api = API(session)
```

## License

**aiookru** is released under the BSD 2-Clause License.
