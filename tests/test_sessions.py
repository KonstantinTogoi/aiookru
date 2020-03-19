import pytest

from aiookru.exceptions import APIError, CustomAPIError
from aiookru.sessions import PublicSession


class TestPublicSession:
    """Tests of PublicSession class."""

    @pytest.mark.asyncio
    async def test_error_request(self, error, error_server):
        async with PublicSession() as session:
            session.API_URL = error_server.url
            session.pass_error = True

            response = await session.public_request()
            assert response == error

    @pytest.mark.asyncio
    async def test_error_request_with_raising(self, error_server):
        async with PublicSession() as session:
            session.API_URL = error_server.url

            session.pass_error = False
            with pytest.raises(APIError):
                await session.public_request()

    @pytest.mark.asyncio
    async def test_dummy_request(self, dummy, dummy_server):
        async with PublicSession() as session:
            session.API_URL = dummy_server.url

            session.pass_error = True
            response = await session.public_request()
            assert response == dummy

    @pytest.mark.asyncio
    async def test_dummy_request_with_raising(self, dummy_server):
        async with PublicSession() as session:
            session.API_URL = dummy_server.url

            session.pass_error = False
            with pytest.raises(CustomAPIError):
                await session.public_request()

    @pytest.mark.asyncio
    async def test_data_request(self, data, data_server):
        async with PublicSession() as session:
            session.API_URL = data_server.url

            session.pass_error = True
            response = await session.public_request()
            assert response == data

            session.pass_error = False
            response = await session.public_request()
            assert response == data
