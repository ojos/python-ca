from typing import Any, List

from ojos_ca.interface.repo import DataStoreRepo
from ojos_ca.usecase import interactor


class BaseInteractor(object):
    def exec(self, *args, **kwargs) -> Any:
        raise NotImplementedError('Not Implemented {}: {}'.format(self.__class__.__name__, 'exec'))

class RepoInteractor(BaseInteractor):
    def __init__(self, repo: DataStoreRepo, *args, **kwargs):
        self._repo = repo

    @property
    def repo(self) -> DataStoreRepo:
        return self._repo

class SerialInterractor(BaseInteractor):
    def __init__(self, interactors: List[BaseInteractor], result_subscript: int=-1) -> Any:
        self._interacotrs = interactors
        self._rs = result_subscript

    def exec(self, *args, **kwargs) -> Any:
        results = [
            i.exec(*args, **kwargs)
            for i in self._interacotrs
        ]
        return results[self._rs]