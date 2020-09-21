from ojos_ca.interface.view.django.sys import(
    SeqView, SysVarView
)
from ojos_ca.usecase.interactor.django import (
    ApiKeyHeaderInteractor, RequestSerialInteractor,
)
from ojos_ca.usecase.interactor.django.sys import (
    GetSeqInteractor, PostSeqInteractor,
    PutSeqInteractor, DeleteSeqInteractor,
    GetSysVarViewInteractor, PostSysVarViewInteractor,
    PutSysVarViewInteractor, DeleteSysVarViewInteractor,
)

from ...repo.django import SeqRepoFactory, SysVarRepoFactory

from .core import BaseViewFactory


class GetSeqInteractorFactory(object):
    @staticmethod
    def get() -> RequestSerialInteractor:
        return RequestSerialInteractor(interactors=[
            ApiKeyHeaderInteractor(),
            GetSeqInteractor(repo=SeqRepoFactory.get())
        ])

class PostSeqInteractorFactory(object):
    @staticmethod
    def get() -> RequestSerialInteractor:
        return RequestSerialInteractor(interactors=[
            ApiKeyHeaderInteractor(),
            PostSeqInteractor(repo=SeqRepoFactory.get())
        ])

class PutSeqInteractorFactory(object):
    @staticmethod
    def get() -> RequestSerialInteractor:
        return RequestSerialInteractor(interactors=[
            ApiKeyHeaderInteractor(),
            PutSeqInteractor(repo=SeqRepoFactory.get())
        ])

class DeleteSeqInteractorFactory(object):
    @staticmethod
    def get() -> RequestSerialInteractor:
        return RequestSerialInteractor(interactors=[
            ApiKeyHeaderInteractor(),
            DeleteSeqInteractor(repo=SeqRepoFactory.get())
        ])

class SeqViewFactory(BaseViewFactory):
    @staticmethod
    def create() -> SeqView:
        return SeqView(
            get_interactor=GetSeqInteractorFactory.get(),
            post_interactor=PostSeqInteractorFactory.get(),
        )

class SeqDetailViewFactory(BaseViewFactory):
    @staticmethod
    def create() -> SeqView:
        return SeqView(
            get_interactor=GetSeqInteractorFactory.get(),
            put_interactor=PutSeqInteractorFactory.get(),
            delete_interactor=DeleteSeqInteractorFactory.get(),
        )

class SysVarViewGetInteractorFactory(object):
    @staticmethod
    def get() -> RequestSerialInteractor:
        return RequestSerialInteractor(interactors=[
            ApiKeyHeaderInteractor(),
            GetSysVarViewInteractor(repo=SysVarRepoFactory.get())
        ])

class SysVarViewPostInteractorFactory(object):
    @staticmethod
    def get() -> RequestSerialInteractor:
        return RequestSerialInteractor(interactors=[
            ApiKeyHeaderInteractor(),
            PostSysVarViewInteractor(repo=SysVarRepoFactory.get())
        ])

class SysVarViewPutInteractorFactory(object):
    @staticmethod
    def get() -> RequestSerialInteractor:
        return RequestSerialInteractor(interactors=[
            ApiKeyHeaderInteractor(),
            PutSysVarViewInteractor(repo=SysVarRepoFactory.get())
        ])

class SysVarViewDeleteInteractorFactory(object):
    @staticmethod
    def get() -> RequestSerialInteractor:
        return RequestSerialInteractor(interactors=[
            ApiKeyHeaderInteractor(),
            DeleteSysVarViewInteractor(repo=SysVarRepoFactory.get())
        ])

class SysVarViewFactory(BaseViewFactory):
    @staticmethod
    def create() -> SysVarView:
        return SysVarView(
            get_interactor=SysVarViewGetInteractorFactory.get(),
            post_interactor=SysVarViewPostInteractorFactory.get(),
        )

class SysVarDetailViewFactory(BaseViewFactory):
    @staticmethod
    def create() -> SysVarView:
        return SysVarView(
            get_interactor=SysVarViewGetInteractorFactory.get(),
            put_interactor=SysVarViewPutInteractorFactory.get(),
            delete_interactor=SysVarViewDeleteInteractorFactory.get(),
        )
