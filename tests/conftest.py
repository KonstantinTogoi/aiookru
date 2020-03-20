import json
from os.path import dirname, join

import pytest

from aiookru.sessions import PublicSession


data_path = join(dirname(__file__), 'data')


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


@pytest.fixture
def auth_dialog():
    with open(join(data_path, 'dialogs', 'auth_dialog.html')) as f:
        return f.read()


@pytest.fixture
def access_dialog():
    with open(join(data_path, 'dialogs', 'access_dialog.html')) as f:
        return f.read()
