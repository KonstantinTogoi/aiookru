import pytest

from aiookru.exceptions import Error, APIError, CustomAPIError
from aiookru.sessions import PublicSession, TokenSession
from aiookru.utils import SignatureCircuit


class TestPublicSession:
    """Tests of PublicSession class."""

    async def test_error_request(self, error, error_server):
        async with PublicSession() as session:
            session.API_URL = error_server.url

            session.pass_error = True
            response = await session.public_request()
            assert response == error

    async def test_error_request_with_raising(self, error_server):
        async with PublicSession() as session:
            session.API_URL = error_server.url

            session.pass_error = False
            with pytest.raises(APIError):
                await session.public_request()

    async def test_dummy_request(self, dummy_server, dummy):
        async with PublicSession() as session:
            session.API_URL = dummy_server.url

            session.pass_error = True
            response = await session.public_request()
            assert response == dummy

    async def test_dummy_request_with_raising(self, dummy_server):
        async with PublicSession() as session:
            session.API_URL = dummy_server.url

            session.pass_error = False
            with pytest.raises(CustomAPIError):
                await session.public_request()

    async def test_data_request(self, data_server, data):
        async with PublicSession() as session:
            session.API_URL = data_server.url

            session.pass_error = True
            response = await session.public_request()
            assert response == data

            session.pass_error = False
            response = await session.public_request()
            assert response == data


class TestTokenSession:
    """Tests of TokenSession class."""

    @pytest.fixture()
    def app(self):
        return {'app_key': 123, 'app_secret_key': ''}

    @pytest.fixture()
    def token(self):
        return {'access_token': '', 'session_secret_key': ''}

    async def test_sig_circuit(self, app, token):
        async with TokenSession(**app, **token) as session:
            assert session.sig_circuit is SignatureCircuit.UNDEFINED

            session.session_secret_key = 'session key'
            assert session.sig_circuit is SignatureCircuit.CLIENT_SERVER

            session.access_token = 'token'
            session.app_secret_key = 'app key'
            assert session.sig_circuit is SignatureCircuit.SERVER_SERVER

    async def test_required_params(self, app, token):
        async with TokenSession(**app, **token) as session:
            assert 'application_key' in session.required_params
            assert 'format' in session.required_params

    async def test_params_to_str(self, app, token):
        async with TokenSession(**app, **token) as session:
            params = {'"a"': 1, '"b"': 2, '"c"': 3}

            with pytest.raises(Error):
                _ = session.params_to_str(params)

            session.session_secret_key = 'session key'
            query = session.params_to_str(params)
            assert query == '"a"=1"b"=2"c"=3session key'

    async def test_error_request(self, app, token, error_server, error):
        async with TokenSession(**app, **token) as session:
            session.API_URL = error_server.url
            session.session_secret_key = 'session key'

            session.pass_error = True
            response = await session.request(params={'key': 'value'})
            assert response == error

    async def test_error_request_with_raising(self, app, token, error_server):
        async with TokenSession(**app, **token) as session:
            session.API_URL = error_server.url
            session.session_secret_key = 'session key'

            session.pass_error = False
            with pytest.raises(APIError):
                _ = await session.request(params={'key': 'value'})

    async def test_dummy_request(self, app, token, dummy_server, dummy):
        async with TokenSession(**app, **token) as session:
            session.API_URL = dummy_server.url
            session.session_secret_key = 'session key'

            session.pass_error = True
            response = await session.request(params={'key': 'value'})
            assert response == dummy

    async def test_dummy_request_with_raising(self, app, token, dummy_server):
        async with TokenSession(**app, **token) as session:
            session.API_URL = dummy_server.url
            session.session_secret_key = 'session key'

            session.pass_error = False
            with pytest.raises(CustomAPIError):
                await session.request(params={'key': 'value'})

    async def test_data_request(self, app, token, data_server, data):
        async with TokenSession(**app, **token) as session:
            session.API_URL = data_server.url
            session.session_secret_key = 'session key'

            session.pass_error = True
            response = await session.request(params={'key': 'value'})
            assert response == data

            session.pass_error = False
            response = await session.request(params={'key': 'value'})
            assert response == data
