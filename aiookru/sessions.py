import aiohttp
import logging

from .exceptions import Error, APIError


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

    PUBLIC_URL = 'https://api.ok.ru/fb.do'
    CONTENT_TYPE = 'application/json;charset=utf-8'

    async def public_request(self, segments=(), params=None):
        """Requests public data.

        Args:
            segments (tuple): additional segments for URL path.
            params (dict): URL parameters.

        Returns:
            response (dict): JSON object response.

        """

        url = f'{self.PUBLIC_URL}/{"/".join(segments)}'

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
