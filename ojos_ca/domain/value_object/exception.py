from ojos.exception import BaseException


class InvalidValueException(BaseException):
    MESSAGE_TEMPLATE = 'Invalid {}: {}'

