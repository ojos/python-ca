import sys
from logging import basicConfig, getLogger, INFO
from typing import Any, Optional

from ojos_ca.usecase.interactor import BaseInteractor
from ojos_ca.usecase.interactor.exception import MethodNotAllowedException

basicConfig()
logger = getLogger(__name__)
logger.setLevel(INFO)


class BaseView(object):
    def __init__(self,
            interactor: Optional[BaseInteractor]=None,
            get_interactor: Optional[BaseInteractor]=None,
            post_interactor: Optional[BaseInteractor]=None,
            put_interactor: Optional[BaseInteractor]=None,
            delete_interactor: Optional[BaseInteractor]=None,
            patch_interactor: Optional[BaseInteractor]=None,
            options_interactor: Optional[BaseInteractor]=None):
        self._interactor = interactor
        self._get_interactor = get_interactor
        self._post_interactor = post_interactor
        self._put_interactor = put_interactor
        self._delete_interactor = delete_interactor
        self._patch_interactor = patch_interactor
        self._options_interactor = options_interactor

    @property
    def get_interactor(self) -> Optional[BaseInteractor]:
        return self._interactor if self._get_interactor is None else self._get_interactor

    @property
    def post_interactor(self) -> Optional[BaseInteractor]:
        return self._interactor if self._post_interactor is None else self._post_interactor

    @property
    def put_interactor(self) -> Optional[BaseInteractor]:
        return self._interactor if self._put_interactor is None else self._put_interactor

    @property
    def delete_interactor(self) -> Optional[BaseInteractor]:
        return self._interactor if self._delete_interactor is None else self._delete_interactor

    @property
    def patch_interactor(self) -> Optional[BaseInteractor]:
        return self._interactor if self._patch_interactor is None else self._patch_interactor

    @property
    def options_interactor(self) -> Optional[BaseInteractor]:
        return self._interactor if self._options_interactor is None else self._options_interactor

    def get(self, *args, **kwargs) -> Any:
        if self.get_interactor is None:
            raise MethodNotAllowedException(name='Method', value='GET')
        return self.get_interactor.exec(*args, **kwargs)

    def post(self, *args, **kwargs) -> Any:
        if self.post_interactor is None:
            raise MethodNotAllowedException(name='Method', value='POST')
        return self.post_interactor.exec(*args, **kwargs)

    def put(self, *args, **kwargs) -> Any:
        if self.put_interactor is None:
            raise MethodNotAllowedException(name='Method', value='PUT')
        return self.put_interactor.exec(*args, **kwargs)

    def delete(self, *args, **kwargs) -> Any:
        if self.delete_interactor is None:
            raise  MethodNotAllowedException(name='Method', value='DELETE')
        return self.delete_interactor.exec(*args, **kwargs)

    def patch(self, *args, **kwargs) -> Any:
        if self.patch_interactor is None:
            raise  MethodNotAllowedException(name='Method', value='PATCH')
        return self.patch_interactor.exec(*args, **kwargs)

    def options(self, *args, **kwargs) -> Any:
        if self.options_interactor is None:
            raise  MethodNotAllowedException(name='Method', value='OPTIONS')
        return self.options_interactor.exec(*args, **kwargs)
