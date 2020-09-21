from logging import basicConfig, getLogger, INFO
from typing import Any

from django.conf import settings
from django.http.request import HttpRequest

from ojos_ca.usecase.interactor.exception import (
    UnauthorizedException
)

from .core import RequestInteractor

basicConfig()
logger = getLogger(__name__)
logger.setLevel(INFO)


class ApiKeyHeaderInteractor(RequestInteractor):
    def exec(self, request: HttpRequest, *args, **kwargs) -> Any:
        host_key = getattr(settings, 'API_KEY', None)
        if host_key is None:
            logger.warning('API_KEY is not set in settings. Disable API KEY auth.')
        else:
            # print(request.META)
            client_key = request.META.get('HTTP_X_API_KEY', None)
            if host_key != client_key:
                raise UnauthorizedException('api key', client_key)