"""Exceptions."""


class Error(Exception):
    """Base exceptions."""

    @property
    def error(self):
        return self.args[0]

    def __init__(self, error: str or dict):
        arg = error if isinstance(error, dict) else {
            'error': 'internal_error',
            'error_description': error,
        }
        super().__init__(arg)


class OAuthError(Error):
    """OAuth error."""

    def __init__(self, error: str):
        super().__init__({'error': 'oauth_error', 'error_description': error})


class CustomOAuthError(Error):
    """Custom errors that raised when authorization failed."""

    ERROR = {'error': '', 'error_description': ''}

    def __init__(self):
        super().__init__(self.ERROR)


class InvalidGrantError(CustomOAuthError):
    """Invalid user credentials."""

    ERROR = {
        'error': 'invalid_grant',
        'error_description': 'invalid login or password',
    }


class InvalidClientError(CustomOAuthError):
    """Invalid client id."""

    ERROR = {
        'error': 'invalid_client',
        'error_description': 'invalid client id',
    }


class InvalidUserError(CustomOAuthError):
    """Invalid user (blocked)."""

    ERROR = {
        'error': 'invalid_user',
        'error_description': 'user is blocked',
    }


class APIError(Error):
    """API exceptions."""

    __slots__ = ('code', 'data', 'msg')

    def __init__(self, error):
        super().__init__(error)
        self.code = error.get('error_code')
        self.data = error.get('error_data')
        self.msg = error.get('error_msg')

    def __str__(self):
        return 'Error {code}: "{msg}". Data: {data}.'.format(
            code=self.code, msg=self.msg, data=self.data
        )
