import sys
from logging import basicConfig, getLogger, INFO
from typing import Any, List

from django.conf import settings
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator

from ojos_ca.di.view import BaseViewFactory
from ojos_ca.usecase.interactor import BaseInteractor
from ojos_ca.usecase.interactor.exception import MethodNotAllowedException
from ojos_ca.usecase.serializer.django import HttpResponseSerializer

from .. import BaseView as _BaseView

basicConfig()
logger = getLogger(__name__)
logger.setLevel(INFO)


class BaseView(_BaseView):
    def get(self, request: HttpRequest, *args, **kwargs) -> Any:
        if self.get_interactor is None:
            raise MethodNotAllowedException(name='Method', value='GET')
        return self.get_interactor.exec(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs) -> Any:
        if self.post_interactor is None:
            raise MethodNotAllowedException(name='Method', value='POST')
        return self.post_interactor.exec(request, *args, **kwargs)

    def put(self, request: HttpRequest, *args, **kwargs) -> Any:
        if self.put_interactor is None:
            raise MethodNotAllowedException(name='Method', value='PUT')
        return self.put_interactor.exec(request, *args, **kwargs)

    def delete(self, request: HttpRequest, *args, **kwargs) -> Any:
        if self.delete_interactor is None:
            raise  MethodNotAllowedException(name='Method', value='DELETE')
        return self.delete_interactor.exec(request, *args, **kwargs)

    def patch(self, request: HttpRequest, *args, **kwargs) -> Any:
        if self.patch_interactor is None:
            raise  MethodNotAllowedException(name='Method', value='PATCH')
        return self.patch_interactor.exec(request, *args, **kwargs)

    def options(self, request: HttpRequest, *args, **kwargs) -> Any:
        if self.options_interactor is None:
            raise  MethodNotAllowedException(name='Method', value='OPTIONS')
        return self.options_interactor.exec(request, *args, **kwargs)


class ViewWrapper(View):
    _view_factory = None
    _serializer   = None
    _allow_method = ['get', 'post', 'put', 'delete', 'patch', 'options']

    @property
    def view_factory(self) -> BaseViewFactory:
        return self._view_factory

    @view_factory.setter
    def view_factory(self, view_factory: BaseViewFactory):
        self._view_factory = view_factory

    @property
    def serializer(self) -> HttpResponseSerializer:
        return self._serializer

    @serializer.setter
    def serializer(self, serializer: HttpResponseSerializer):
        self._serializer = serializer

    @property
    def allow_method(self) -> List[str]:
        return self._allow_method

    @allow_method.setter
    def allow_method(self, allow_method: List[str]):
        self._allow_method = allow_method


    def http_method_not_allowed(self, request, *args, **kwargs):
        raise MethodNotAllowedException(name='method', value=request.method)

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        method = request.method.lower()
        if method in self.http_method_names and method in self.allow_method:
            handler = getattr(self.view_factory.create(), method, self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        # kwargs = handler(request, *args, **kwargs)
        # return self.serializer.to_response(**kwargs)

        try:
            kwargs = handler(request, *args, **kwargs)
            return self.serializer.to_response(**kwargs)
        except Exception as e:
            logger.error(e)
            return self.serializer.error_to_response(e)


@method_decorator(csrf_exempt, name='dispatch')
class ApiViewWrapper(ViewWrapper):
    ACCESS_CONTROL_ALLOW_ORIGIN      = getattr(settings, 'ACCESS_CONTROL_ALLOW_ORIGIN', '*')
    ACCESS_CONTROL_ALLOW_METHODS     = getattr(settings, 'ACCESS_CONTROL_ALLOW_METHODS', 'GET,POST,PUT,DELETE,PATCH,OPTIONS')
    ACCESS_CONTROL_ALLOW_HEADERS     = getattr(settings, 'ACCESS_CONTROL_ALLOW_HEADERS', 'Origin,Authorization,Accept,Content-Type')
    ACCESS_CONTROL_MAX_AGE           = getattr(settings, 'ACCESS_CONTROL_MAX_AGE', 3600)
    ACCESS_CONTROL_ALLOW_CREDENTIALS = True

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        method = request.method.lower()
        if method == 'options':
            response = self.serializer.to_response(status_code=204)
        else:
            response = super(ApiViewWrapper, self).dispatch(request, *args, **kwargs)
        response['Access-Control-Allow-Origin'] = self.ACCESS_CONTROL_ALLOW_ORIGIN

        if self.ACCESS_CONTROL_ALLOW_ORIGIN != '*' and \
                self.ACCESS_CONTROL_ALLOW_CREDENTIALS:
            response['Access-Control-Allow-Credentials'] = True

        if method == 'options':
            response['Access-Control-Allow-Methods'] = self.ACCESS_CONTROL_ALLOW_METHODS
            response['Access-Control-Allow-Hegetattraders'] = self.ACCESS_CONTROL_ALLOW_HEADERS
            response['Access-Control-Max-Age'] = self.ACCESS_CONTROL_MAX_AGE

        return response

