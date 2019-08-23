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


class APIError(Error):
    """API exceptions."""

    __slots__ = ('code', 'data', 'msg')

    def __init__(self, error):
        super().__init__(error)
        self.code = error.get('error_code')
        self.data = error.get('error_data')
        self.msg = error.get('error_msg')

    def __str__(self):
        return f'Error {self.code}: "{self.msg}". Data: {self.data}.'


class AuthError(Error):
    ERROR = {
        'error': 'invalid_user_credentials',
        'error_description': 'invalid login or password',
    }

    def __init__(self):
        super().__init__(self.ERROR)


class OKAuthError(Error):
    """Error 401."""

    def __init__(self, error: dict):
        super().__init__(error)
