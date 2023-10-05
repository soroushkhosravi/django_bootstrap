class ServiceException(Exception):
    """Raised when a service exception happens."""


class SerializerException(Exception):
    """Raised when a serializer is not able to validate data."""
    def __init__(self, message: str, errors: dict):
        """Instantiates the error object."""
        super().__init__(message + str(errors))
