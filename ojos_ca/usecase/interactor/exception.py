from logging import basicConfig, getLogger, INFO

from ojos.exception import BaseException


class ResponseException(BaseException):
    STATUS_CODE = 500
    MESSAGE_TEMPLATE = '{} Error {}: {}'

    def __init__(self, name: str=None, value=None, status_code: int=None, message: str=None, **kwargs):
        self.status_code = self.STATUS_CODE if status_code is None else status_code
        self.message = self.MESSAGE_TEMPLATE.format(self.status_code, name, value) if message is None else message
        # super(ResponseException, self).__init__(name=name, value=value, **kwargs)


class BadRequestException(ResponseException):
    STATUS_CODE = 400
    MESSAGE_TEMPLATE = '{} Bad Request {}:{}'


class UnauthorizedException(ResponseException):
    STATUS_CODE = 401
    MESSAGE_TEMPLATE = '{} Unauthorized {}:{}'


class PaymentRequiredException(ResponseException):
    STATUS_CODE = 402
    MESSAGE_TEMPLATE = '{} Payment Required {}:{}'


class ForbiddenException(ResponseException):
    STATUS_CODE = 403
    MESSAGE_TEMPLATE = '{} Forbidden {}: {}'


class NotFoundException(ResponseException):
    STATUS_CODE = 404
    MESSAGE_TEMPLATE = '{} Not Found {}: {}'


class MethodNotAllowedException(ResponseException):
    STATUS_CODE = 405
    MESSAGE_TEMPLATE = '{} Method Not Allowed {}: {}'


class NotAcceptableException(ResponseException):
    STATUS_CODE = 406
    MESSAGE_TEMPLATE = '{} Not Acceptable {}: {}'


class ProxyAuthenticationRequiredException(ResponseException):
    STATUS_CODE = 407
    MESSAGE_TEMPLATE = '{} Proxy Authentication Required {}: {}'


class RequestTimeoutException(ResponseException):
    STATUS_CODE = 408
    MESSAGE_TEMPLATE = '{} Request Timeout {}: {}'


class ConflictException(ResponseException):
    STATUS_CODE = 409
    MESSAGE_TEMPLATE = '{} Conflict {}: {}'


class GoneException(ResponseException):
    STATUS_CODE = 410
    MESSAGE_TEMPLATE = '{} Gone {}: {}'


class LengthRequiredException(ResponseException):
    STATUS_CODE = 411
    MESSAGE_TEMPLATE = '{} Length Required {}: {}'


class PreconditionFailedException(ResponseException):
    STATUS_CODE = 412
    MESSAGE_TEMPLATE = '{} Precondition Failed {}: {}'


class RequestEntityTooLargeException(ResponseException):
    STATUS_CODE = 413
    MESSAGE_TEMPLATE = '{} Payload Too Large {}: {}'


class RequestUriTooLongException(ResponseException):
    STATUS_CODE = 414
    MESSAGE_TEMPLATE = '{} URI Too Long {}: {}'


class UnsupportedMediaTypeException(ResponseException):
    STATUS_CODE = 415
    MESSAGE_TEMPLATE = '{} Unsupported Media Type {}: {}'


class RequestedRangeNotSatisfiableException(ResponseException):
    STATUS_CODE = 416
    MESSAGE_TEMPLATE = '{} Range Not Satisfiable {}: {}'


class ExpectationFailedException(ResponseException):
    STATUS_CODE = 417
    MESSAGE_TEMPLATE = '{} Expectation Failed {}: {}'


class InternalServerErrorException(ResponseException):
    STATUS_CODE = 500
    MESSAGE_TEMPLATE = '{} Internal Server Error {}: {}'


class NotImplementedException(ResponseException):
    STATUS_CODE = 501
    MESSAGE_TEMPLATE = '{} Not Implemented {}: {}'


class BadGatewayException(ResponseException):
    STATUS_CODE = 502
    MESSAGE_TEMPLATE = '{} Bad Gateway {}: {}'


class ServiceUnavailableException(ResponseException):
    STATUS_CODE = 503
    MESSAGE_TEMPLATE = '{} Service Unavailable {}: {}'


class GatewayTimeoutException(ResponseException):
    STATUS_CODE = 504
    MESSAGE_TEMPLATE = '{} Gateway Timeout {}: {}'