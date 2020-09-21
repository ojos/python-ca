from typing import Any

from ojos.exception import BaseException


class DoesNotExistException(BaseException):
    MESSAGE_TEMPLATE = 'Does not exist {}: {}'


class DuplicateEntryException(BaseException):
    MESSAGE_TEMPLATE = 'Duplicate entry {}: {}'


class DidNotSaveException(BaseException):
    MESSAGE_TEMPLATE = 'Did not save {}: {}'

