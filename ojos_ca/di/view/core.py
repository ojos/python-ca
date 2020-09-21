from ojos_ca.interface.view import BaseView
from ojos_ca.usecase.interactor import BaseInteractor

class BaseViewFactory(object):
    @staticmethod
    def create() -> BaseView:
        interactor = BaseInteractor()
        return BaseView(interactor=interactor)