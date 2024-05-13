class Error(Exception):
    error_code = None
    error_message = None
    error_detailed = None
    status_code = None

    def __init__(self, error_message):
        Exception.__init__(self)
        self.error_message = error_message

    def to_dict(self):
        return {
            'code': self.error_code,
            'error_message': self.error_message,
            'error_detailed': self.error_detailed
        }


class InputValidationError(Error):
    """Raised when there is either a missing field or bad data type for field"""

    def __init__(self, error_detailed=None, status_code=400):
        self.error_detailed = error_detailed
        self.error_code = 'P-01'
        self.error_message = "A Required Field is missing or is an invalid data type."
        self.status_code = status_code


class DoesNotExist(Error):
    """Raised when there is no record found in the database."""

    def __init__(self, error_detailed=None, status_code=404):
        self.error_detailed = error_detailed
        self.error_code = 'P-02'
        self.error_message = "Not found"
        self.status_code = status_code


class WrongPassword(Error):
    """Raised when the password is incorrect"""

    def __init__(self, error_detailed=None, status_code=404):
        self.error_detailed = error_detailed
        self.error_code = 'P-03'
        self.error_message = "Wrong password"
        self.status_code = status_code


class Unauthorized(Error):
    """Raised when the token is not correct"""

    def __init__(self, error_detailed=None, status_code=401):
        self.error_detailed = error_detailed
        self.error_code = 'P-04'
        self.error_message = "Unauthorized"
        self.status_code = status_code


class DuplicateUser(Error):
    """Raised when there is a duplicate user"""

    def __init__(self, error_detailed=None, status_code=401):
        self.error_detailed = error_detailed
        self.error_code = 'P-05'
        self.error_message = "there's User with the same information"
        self.status_code = status_code
