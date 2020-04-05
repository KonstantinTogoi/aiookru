"""Exceptions."""


class Error(Exception):
    """Base exceptions."""

    ERROR = 'internal_error'

    @property
    def error(self):
        return self.args[0]

    def __init__(self, error: str or dict):
        arg = error if isinstance(error, dict) else {
            'error': self.ERROR,
            'error_description': error,
        }
        super().__init__(arg)


class OAuthError(Error):
    """OAuth error."""

    ERROR = 'oauth_error'


class CustomOAuthError(OAuthError):
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
    """API error."""

    def __init__(self, error: dict):
        super().__init__(error)
        self.code = error.get('error_code')
        self.data = error.get('error_data')
        self.msg = error.get('error_msg')

    def __str__(self):
        return 'Error {code}: "{msg}". Data: {data}.'.format(
            code=self.code, msg=self.msg, data=self.data
        )


class CustomAPIError(APIError):
    """Custom API error."""

    ERROR = {'error_code': 0, 'error_data': {}, 'error_msg': ''}

    def __init__(self):
        super().__init__(self.ERROR)


class EmptyResponseError(CustomAPIError):
    """Empty API response."""

    ERROR = {'error_code': -1, 'error_data': {}, 'error_msg': 'empty response'}
