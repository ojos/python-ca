from ojos_ca.interface.view.django import BaseView
from ojos_ca.usecase.interactor.django import RequestInteractor

class BaseViewFactory(object):
    @staticmethod
    def create() -> BaseView:
        interactor = RequestInteractor()
        return BaseView(interactor=interactor)