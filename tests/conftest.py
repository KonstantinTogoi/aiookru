import json
import pytest

from aiookru.sessions import (
    PublicSession,
)


@pytest.fixture
def error():
    return {'error_code': -1, 'error_msg': 'test error msg'}


@pytest.fixture
def dummy():
    return {}


@pytest.fixture
def data():
    return {'key': 'value'}


@pytest.yield_fixture
async def error_server(httpserver, error):
    httpserver.serve_content(**{
        'code': 401,
        'headers': {'Content-Type': PublicSession.CONTENT_TYPE},
        'content': json.dumps(error),
    })
    return httpserver


@pytest.yield_fixture
async def dummy_server(httpserver, dummy):
    httpserver.serve_content(**{
        'code': 401,
        'headers': {'Content-Type': PublicSession.CONTENT_TYPE},
        'content': json.dumps(dummy),
    })
    return httpserver


@pytest.yield_fixture
async def data_server(httpserver, data):
    httpserver.serve_content(**{
        'code': 401,
        'headers': {'Content-Type': PublicSession.CONTENT_TYPE},
        'content': json.dumps(data),
    })
    return httpserver
