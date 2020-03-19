"""ok.ru API."""

from .sessions import TokenSession


class API:
    """ok.ru API."""

    __slots__ = ('session', )

    def __init__(self, session: TokenSession):
        self.session = session

    def __getattr__(self, name):
        return APIMethod(self, name)

    async def __call__(self, name, **params):
        return await getattr(self, name)(**params)


class APIMethod:
    """ok.ru REST API method."""

    __slots__ = ('api', 'name')

    def __init__(self, api: API, name: str):
        self.api = api
        self.name = name

    def __getattr__(self, name):
        return APIMethod(self.api, self.name + '.' + name)

    async def __call__(self, *args, **params):
        params['method'] = self.name
        return await self.api.session.request(params=params)
