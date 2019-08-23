import aiohttp
import logging
from hashlib import md5

from .exceptions import Error, APIError
from .utils import SignatureCircuit


log = logging.getLogger(__name__)


class Session:
    """A wrapper around aiohttp.ClientSession."""

    __slots__ = ('pass_error', 'session')

    def __init__(self, pass_error=False, session=None):
        self.pass_error = pass_error
        self.session = session or aiohttp.ClientSession()

    def __await__(self):
        return self.authorize().__await__()

    async def __aenter__(self):
        return await self.authorize()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def authorize(self):
        return self

    async def close(self):
        await self.session.close()


class PublicSession(Session):
    """Session for calling public API methods of OK API."""

    API_URL = 'https://api.ok.ru/fb.do'
    CONTENT_TYPE = 'application/json;charset=utf-8'

    async def public_request(self, segments=(), params=None):
        """Requests public data.

        Args:
            segments (tuple): additional segments for URL path.
            params (dict): URL parameters.

        Returns:
            response (dict): JSON object response.

        """

        segments = f'/{"/".join(segments)}' if segments else ''
        url = f'{self.API_URL}{segments}'

        try:
            async with self.session.get(url, params=params) as resp:
                content = await resp.json(content_type=self.CONTENT_TYPE)
        except aiohttp.ContentTypeError:
            msg = f'got non-REST path: {url}'
            log.error(msg)
            raise Error(msg)

        if self.pass_error:
            response = content
        elif 'error_code' in content:
            log.error(content)
            raise APIError(content)
        else:
            response = content

        return response


class TokenSession(PublicSession):
    """Session for sending authorized requests."""

    ERROR_MSG = 'See calculating signature at https://apiok.ru/dev/methods/.'

    __slots__ = ('app_key', 'app_secret_key', 'access_token',
                 'session_secret_key', 'format')

    def __init__(self, app_key, app_secret_key='', access_token='',
                 session_secret_key='', format='json',
                 pass_error=False, session=None):
        super().__init__(pass_error, session)
        self.app_key = app_key
        self.app_secret_key = app_secret_key
        self.access_token = access_token
        self.session_secret_key = session_secret_key
        self.format = format

    @property
    def required_params(self):
        """Required parameters."""
        return {'application_key': self.app_key, 'format': self.format}

    @property
    def sig_circuit(self):
        if self.session_secret_key and self.app_key:
            return SignatureCircuit.CLIENT_SERVER
        elif self.app_secret_key and self.access_token and self.app_key:
            return SignatureCircuit.SERVER_SERVER
        else:
            return SignatureCircuit.UNDEFINED

    @property
    def secret_key(self):
        if self.sig_circuit is SignatureCircuit.CLIENT_SERVER:
            return self.session_secret_key
        elif self.sig_circuit is SignatureCircuit.SERVER_SERVER:
            plain = f'{self.access_token}{self.app_secret_key}'
            return md5(plain.encode('utf-8')).hexdigest().lower()
        else:
            raise Error(self.ERROR_MSG)

    def params_to_str(self, params):
        query = ''.join(f'{k}={str(params[k])}' for k in sorted(params))
        return f'{query}{self.secret_key}'

    def sign_params(self, params):
        query = self.params_to_str(params)
        return md5(query.encode('utf-8')).hexdigest()

    async def request(self, segments=(), params=()):
        segments = f'/{"/".join(segments)}' if segments else ''
        url = f'{self.API_URL}{segments}'

        params = {k: params[k] for k in params if params[k]}
        params.update(self.required_params)
        params.update({'sig': self.sign_params(params)})

        async with self.session.get(url, params=params) as resp:
            content = await resp.json(content_type=self.CONTENT_TYPE)

        if self.pass_error:
            response = content
        elif 'error_code' in content:
            log.error(content)
            raise APIError(content)
        else:
            response = content

        return response


class ClientSession(TokenSession):

    ERROR_MSG = 'Pass "session_secret_key" to use client-server circuit.'

    def __init__(self, app_key, session_secret_key,
                 format='json', pass_error=False, session=None):
        super().__init__(app_key, '', '', session_secret_key,
                         format=format, pass_error=pass_error, session=session)


class ServerSession(TokenSession):

    ERROR_MSG = 'Pass "app_secret_key" and "access_token" ' \
                'to use server-server circuit.'

    def __init__(self, app_key, app_secret_key, access_token,
                 format='json', pass_error=False, session=None):
        super().__init__(app_key, app_secret_key, access_token, '',
                         format=format, pass_error=pass_error, session=session)


class WebSession(PublicSession):

    def __init__(self, app_key, session_key, session_secret_key,
                 format='json', pass_error=False, session=None):
        super().__init__(pass_error, session)
        self.app_key = app_key
        self.session_key = session_key
        self.session_secret_key = session_secret_key
        self.format = format


class ImplicitWebSession(WebSession):

    __slots__ = ('login', 'passwd')

    def __init__(self, app_key, login, passwd,
                 format='json', pass_error=False, session=None):
        super().__init__(app_key, '', '', format, pass_error, session)
        self.login = login
        self.passwd = passwd

    @property
    def params(self):
        """Authorization parameters."""
        return {
            'method': 'auth.login',
            'application_key': self.app_key,
            'user_name': self.login,
            'password': self.passwd,
            'verification_supported': 1,
            'verification_supported_v': 1,
            'format': 'json',
        }

    async def authorize(self):
        resp = await self.public_request(params=self.params)

        if self.pass_error and 'error_code' in resp:
            log.error(resp)
            raise APIError(resp)
        else:
            self.session_key = resp['session_key']
            self.session_secret_key = resp['session_secret_key']
