from typing import Any, List

from django.http.request import HttpRequest

from .. import BaseInteractor, SerialInterractor


class RequestInteractor(BaseInteractor):
    def exec(self, request: HttpRequest, *args, **kwargs) -> Any:
        raise NotImplementedError('Not Implemented {}: {}'.format(self.__class__.__name__, 'exec'))

class RequestSerialInteractor(SerialInterractor):
    def __init__(self, interactors: List[RequestInteractor], result_subscript: int=-1) -> Any:
        super(RequestSerialInteractor, self).__init__(interactors, result_subscript)

    def exec(self, request: HttpRequest, *args, **kwargs) -> Any:
        results = [
            i.exec(request, *args, **kwargs)
            for i in self._interacotrs
        ]
        return results[self._rs]
