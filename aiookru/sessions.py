import asyncio
import logging
from hashlib import md5

import aiohttp
from yarl import URL

from .exceptions import (
    Error,
    OAuthError,
    InvalidGrantError,
    APIError,
    EmptyResponseError,
)
from .utils import SignatureCircuit
from .parsers import AuthDialogParser, AccessDialogParser


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

        segments = '/' + '/'.join(segments) if segments else ''
        url = self.API_URL + segments

        try:
            async with self.session.get(url, params=params) as resp:
                content = await resp.json(content_type=self.CONTENT_TYPE)
        except aiohttp.ContentTypeError:
            msg = 'got non-REST path: %s' % url
            log.error(msg)
            raise Error(msg)

        if self.pass_error:
            response = content
        elif 'error_code' in content:
            log.error(content)
            raise APIError(content)
        elif content:
            response = content
        else:
            log.error('got empty response: %s' % url)
            raise EmptyResponseError()

        return response


class TokenSession(PublicSession):
    """Session for executing authorized requests."""

    ERROR_MSG = 'See calculating signature at https://apiok.ru/dev/methods/.'

    __slots__ = (
        'app_id', 'app_key', 'app_secret_key',
        'access_token', 'session_secret_key', 'format'
    )

    def __init__(self, app_id, app_key, app_secret_key,
                 access_token, session_secret_key,
                 format='json', pass_error=False, session=None, **kwargs):
        super().__init__(pass_error, session)
        self.app_id = app_id
        self.app_key = app_key
        self.app_secret_key = app_secret_key
        self.access_token = access_token
        self.session_secret_key = session_secret_key
        self.format = format

    @property
    def session_key(self):
        return self.access_token

    @session_key.setter
    def session_key(self, session_key):
        self.access_token = session_key

    @property
    def required_params(self):
        """Required parameters."""
        return {'application_key': self.app_key, 'format': self.format}

    @property
    def sig_circuit(self):
        if self.app_secret_key and self.access_token and self.app_key:
            return SignatureCircuit.SERVER_SERVER
        elif self.session_secret_key and self.access_token and self.app_key:
            return SignatureCircuit.CLIENT_SERVER
        else:
            return SignatureCircuit.UNDEFINED

    @property
    def secret_key(self):
        if self.sig_circuit is SignatureCircuit.CLIENT_SERVER:
            return self.session_secret_key
        elif self.sig_circuit is SignatureCircuit.SERVER_SERVER:
            plain = self.access_token + self.app_secret_key
            return md5(plain.encode('utf-8')).hexdigest().lower()
        else:
            raise Error(self.ERROR_MSG)

    def params_to_str(self, params):
        query = ''.join(k + '=' + str(params[k]) for k in sorted(params))
        return query + self.secret_key

    def sign_params(self, params):
        query = self.params_to_str(params)
        return md5(query.encode('utf-8')).hexdigest()

    async def request(self, segments=(), params=()):
        """Sends a request.

        Args:
            segments (tuple): additional segments for URL path.
            params (dict): URL parameters

        Returns:
            response (dict): JSON object response.

        """
        segments = '/' + '/'.join(segments) if segments else ''
        url = self.API_URL + segments

        params = {k: params[k] for k in params if params[k]}
        params.update(self.required_params)
        params.update({
            'sig': self.sign_params(params),
            'access_token': self.access_token,
        })

        async with self.session.get(url, params=params) as resp:
            content = await resp.json(content_type=self.CONTENT_TYPE)

        if self.pass_error:
            response = content
        elif 'error_code' in content:
            log.error(content)
            raise APIError(content)
        elif content:
            response = content
        else:
            log.error('got empty response: %s' % url)
            raise EmptyResponseError()

        return response


class ClientSession(TokenSession):
    """Session for executing requests in client applications.

    `TokenSession` without `app_secret_key` argument.

    """

    ERROR_MSG = (
        'Pass "session_secret_key" and "access_token"'
        'to use client-server circuit.'
    )

    def __init__(self, app_id, app_key, access_token, session_secret_key,
                 format='json', pass_error=False, session=None, **kwargs):
        super().__init__(app_id, app_key, '', access_token, session_secret_key,
                         format, pass_error, session, **kwargs)


class ServerSession(TokenSession):
    """Session for executing requests in server applications.

    `TokenSession` without `session_secret_key` argument.

    """

    ERROR_MSG = (
        'Pass "app_secret_key" and "access_token"'
        'to use server-server circuit.'
    )

    def __init__(self, app_id, app_key, app_secret_key, access_token,
                 format='json', pass_error=False, session=None, **kwargs):
        super().__init__(app_id, app_key, app_secret_key, access_token, '',
                         format, pass_error, session, **kwargs)


class CodeSession(TokenSession):
    """Session with authorization with OAuth 2.0 (Authorization Code Grant).

    The Authorization Code grant is used by confidential and public
    clients to exchange an authorization code for an access token.

    .. _OAuth 2.0 Authorization Code Grant
        https://oauth.net/2/grant-types/authorization-code/

    .. _Серверная OAuth авторизация
        https://apiok.ru/ext/oauth/server

    """

    OAUTH_URL = 'https:/api.ok.ru/oauth/token.do'

    __slots__ = (
        'code', 'redirect_uri', 'refresh_token', 'token_type', 'expires_in'
    )

    def __init__(self, app_id, app_key, app_secret_key, code, redirect_uri,
                 format='json', pass_error=False, session=None, **kwargs):
        super().__init__(app_id, app_key, app_secret_key, '', '',
                         format, pass_error, session, **kwargs)
        self.code = code
        self.redirect_uri = redirect_uri

    @property
    def params(self):
        """Authorization request's parameters."""
        return {
            'code': self.code,
            'client_id': self.app_id,
            'client_secret': self.secret_key,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code',
        }

    async def authorize(self):
        """Authorize with OAuth 2.0 (Authorization Code)."""

        async with self.session.post(self.OAUTH_URL, data=self.params) as resp:
            content = await resp.json(content_type=self.CONTENT_TYPE)

        if 'error' in content:
            log.error(content)
            raise OAuthError(content)
        elif content:
            try:
                self.access_token = content['access_token']
                self.token_type = content.get('token_type')
                self.refresh_token = content['refresh_token']
                self.expires_in = content.get('expires_in')
            except KeyError as e:
                raise OAuthError(str(e.args[0]) + ' is missing in the response')
        else:
            raise OAuthError('got empty authorization response')

        return self


class CodeServerSession(CodeSession):
    """The same as `CodeSession`."""


class ImplicitSession(TokenSession):
    """Session with authorization with OAuth 2.0 (Implicit Grant).

    The Implicit flow was a simplified OAuth flow previously recommended
    for native apps and JavaScript apps where the access token was returned
    immediately without an extra authorization code exchange step.

    .. _OAuth 2.0 Implicit Grant
        https://oauth.net/2/grant-types/implicit/

    .. _Клиентская OAuth авторизация
        https://apiok.ru/ext/oauth/client

    """

    CONNECT_URL = 'https://connect.ok.ru'
    OAUTH_URL = CONNECT_URL + '/oauth/authorize'
    REDIRECT_URI = 'https://oauth.mycdn.me/blank.html'

    GET_AUTH_DIALOG_ERROR_MSG = 'Failed to open authorization dialog.'
    POST_AUTH_DIALOG_ERROR_MSG = 'Form submission failed.'
    GET_ACCESS_TOKEN_ERROR_MSG = 'Failed to receive access token.'
    POST_ACCESS_DIALOG_ERROR_MSG = 'Failed to process access dialog.'

    AUTHORIZE_NUM_ATTEMPTS = 1
    AUTHORIZE_RETRY_INTERVAL = 1

    __slots__ = ('login', 'passwd', 'scope', 'redirect_uri', 'state',
                 'expires_in', 'permissions_granted')

    def __init__(self, app_id, app_key, app_secret_key,
                 login, passwd, scope='', redirect_uri='', state='',
                 format='json', pass_error=False, session=None, **kwargs):
        super().__init__(app_id, app_key, app_secret_key, '', '',
                         format, pass_error, session, **kwargs)
        self.login = login
        self.passwd = passwd
        self.scope = scope
        self.redirect_uri = redirect_uri or self.REDIRECT_URI
        self.state = state

    @property
    def params(self):
        """Authorization request's parameters."""
        return {
            'client_id': self.app_id,
            'scope': self.scope,
            'response_type': 'token',
            'redirect_uri': self.redirect_uri,
            'layout': 'w',
            'state': self.state,
        }

    async def authorize(self, num_attempts=None, retry_interval=None):
        """Authorize with OAuth 2.0 (Implicit flow)."""

        num_attempts = num_attempts or self.AUTHORIZE_NUM_ATTEMPTS
        retry_interval = retry_interval or self.AUTHORIZE_RETRY_INTERVAL

        for attempt_num in range(num_attempts):
            log.debug('getting authorization dialog ' + self.OAUTH_URL)
            url, html = await self._get_auth_dialog()

            st_cmd = url.query.get('st.cmd')
            if url.path == '/dk' and st_cmd == 'OAuth2Login':
                log.debug('authorizing at {url}'.format(url=url))
                url, html = await self._post_auth_dialog(html)

            st_cmd = url.query.get('st.cmd')
            if url.path == '/dk' and st_cmd == 'OAuth2Permissions':
                log.debug('giving permissions at {url}'.format(url=url))
                url, html = await self._post_access_dialog(html)
            elif url.path == '/dk' and st_cmd == 'OAuth2Login':
                log.error('Invalid login or password.')
                raise InvalidGrantError()

            if url.path == '/blank.html':
                log.debug('authorized successfully')
                await self._get_access_token()
                return self

            await asyncio.sleep(retry_interval)
        else:
            log.error('%d login attempts exceeded.' % num_attempts)
            raise OAuthError('%d login attempts exceeded.' % num_attempts)

    async def _get_auth_dialog(self):
        """Return URL and html code of authorization page."""

        async with self.session.get(self.OAUTH_URL, params=self.params) as resp:
            if resp.status == 401:
                error = await resp.json(content_type=self.CONTENT_TYPE)
                log.error(error)
                raise Error(error)
            elif resp.status != 200:
                log.error(self.GET_AUTH_DIALOG_ERROR_MSG)
                raise OAuthError(self.GET_AUTH_DIALOG_ERROR_MSG)
            else:
                url, html = resp.url, await resp.text()

        return url, html

    async def _post_auth_dialog(self, html):
        """Submits a form with login and password to get access token."""

        parser = AuthDialogParser()
        parser.feed(html)
        parser.close()

        form_url, form_data = parser.form
        form_url = self.CONNECT_URL + form_url
        form_data['fr.email'] = self.login
        form_data['fr.password'] = self.passwd

        async with self.session.post(form_url, data=form_data) as resp:
            if resp.status != 200:
                # TODO: parse error in URL
                log.error(self.POST_AUTH_DIALOG_ERROR_MSG)
                raise OAuthError(self.POST_AUTH_DIALOG_ERROR_MSG)
            else:
                url, html = resp.url, await resp.text()

        return url, html

    async def _post_access_dialog(self, html):
        """Clicks button 'allow' in an access dialog."""

        parser = AccessDialogParser()
        parser.feed(html)
        parser.close()

        form_url, form_data = parser.form
        form_url = self.CONNECT_URL + form_url
        form_data['button_accept_request'] = ''

        async with self.session.post(form_url, data=form_data) as resp:
            if resp.status != 200:
                log.error(self.POST_ACCESS_DIALOG_ERROR_MSG)
                raise OAuthError(self.POST_ACCESS_DIALOG_ERROR_MSG)
            else:
                url, html = resp.url, await resp.text()

        return url, html

    async def _get_access_token(self):
        async with self.session.get(self.OAUTH_URL, params=self.params) as resp:
            if resp.status != 200:
                log.error(self.GET_ACCESS_TOKEN_ERROR_MSG)
                raise OAuthError(self.GET_ACCESS_TOKEN_ERROR_MSG)
            else:
                location = URL(resp.history[-1].headers['Location'])
                url = URL('?' + location.fragment)

        try:
            self.access_token = url.query['access_token']
            self.session_secret_key = url.query['session_secret_key']
            self.state = url.query.get('state')
            self.permissions_granted = url.query.get('permissions_granted')
            self.expires_in = url.query.get('expires_in')
        except KeyError as e:
            raise OAuthError(str(e.args[0]) + ' is missing in the response.')


class ImplicitClientSession(ImplicitSession):
    """`ImplicitSession` without `app_secret_key` argument."""

    def __init__(self, app_id, app_key, login, passwd,
                 scope='', redirect_uri='', state='',
                 format='json', pass_error=False, session=None, **kwargs):
        super().__init__(app_id, app_key, '', login, passwd,
                         scope, redirect_uri, state,
                         format, pass_error, session, **kwargs)


class PasswordSession(TokenSession):
    """Session with authorization with OAuth 2.0 (Password Grant).

    The Password grant type is a way to exchange a user's credentials
    for an access token.

    .. _OAuth 2.0 Password Grant
        https://oauth.net/2/grant-types/password/

    """

    __slots__ = ('login', 'passwd')

    def __init__(self, app_id, app_key, app_secret_key, login, passwd,
                 format='json', pass_error=False, session=None, **kwargs):
        super().__init__(app_id, app_key, app_secret_key, '', '',
                         format, pass_error, session, **kwargs)
        self.login = login
        self.passwd = passwd

    @property
    def params(self):
        """Authorization request's parameters."""
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
        """Authorize with OAuth 2.0 (Password Grant)."""

        async with self.session.get(self.API_URL, params=self.params) as resp:
            content = await resp.json(content_type=self.CONTENT_TYPE)

        if 'error_code' in content:
            log.error(content)
            raise APIError(content)
        elif content:
            self.access_token = content['session_key']
            self.session_secret_key = content['session_secret_key']
        else:
            raise OAuthError('got empty authorization response')

        return self


class PasswordClientSession(PasswordSession):
    """`PasswordSession` without `app_secret_key` argument."""

    def __init__(self, app_id, app_key, login, passwd,
                 format='json', pass_error=False, session=None, **kwargs):
        super().__init__(app_id, app_key, '', login, passwd,
                         format, pass_error, session, **kwargs)


class RefreshSession(TokenSession):
    """Session with authorization with OAuth 2.0 (Refresh Token).

    The Refresh Token grant type is used by clients to exchange
    a refresh token for an access token when the access token has expired.

    .. _OAuth 2.0 Refresh Token
        https://oauth.net/2/grant-types/refresh-token/

    .. _Использование refresh_token
        https://apiok.ru/ext/oauth/server

    """

    OAUTH_URL = 'https://api.ok.ru/oauth/token.do'

    __slots__ = ('refresh_token', 'token_type', 'expires_in')

    def __init__(self, app_id, app_key, app_secret_key, refresh_token,
                 format='json', pass_error=False, session=None, **kwargs):
        super().__init__(app_id, app_key, app_secret_key, '', '',
                         format, pass_error, session, **kwargs)
        self.refresh_token = refresh_token

    @property
    def params(self):
        """Authorization request's parameters."""
        return {
            'refresh_token': self.refresh_token,
            'client_id': self.app_id,
            'client_secret': self.secret_key,
            'grant_type': 'refresh_token',
        }

    async def authorize(self):
        """Authorize with OAuth 2.0 (Refresh Token)."""

        async with self.session.post(self.OAUTH_URL, data=self.params) as resp:
            content = await resp.json(content_type=self.CONTENT_TYPE)

        if 'error' in content:
            log.error(content)
            raise OAuthError(content)
        elif content:
            try:
                self.access_token = content['access_token']
                self.token_type = content.get('token_type')
                self.expires_in = content.get('expires_in')
            except KeyError as e:
                raise OAuthError(str(e.args[0]) + ' is missing in the response')
        else:
            raise OAuthError('got empty authorization response')

        return self


class RefreshServerSession(RefreshSession):
    """The same as `RefreshSession`."""
