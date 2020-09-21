from django.urls import path

from ojos_ca.di.view.django import (
    SeqViewFactory, SeqDetailViewFactory,
    SysVarViewFactory, SysVarDetailViewFactory
)
from ojos_ca.interface.view.django import (
    ApiViewWrapper
)
from ojos_ca.usecase.serializer.django import (
    JsonApiResponseSerializer
)

urlpatterns = [
    path(
        r'seq',
        ApiViewWrapper.as_view(
            view_factory=SeqViewFactory,
            serializer=JsonApiResponseSerializer
        )
    ),
    path(
        r'seq/<str:seq_id>',
        ApiViewWrapper.as_view(
            view_factory=SeqDetailViewFactory,
            serializer=JsonApiResponseSerializer
        )
    ),
    path(
        r'var',
        ApiViewWrapper.as_view(
            view_factory=SysVarViewFactory,
            serializer=JsonApiResponseSerializer
        )
    ),
    path(
        r'var/<str:key>',
        ApiViewWrapper.as_view(
            view_factory=SysVarDetailViewFactory,
            serializer=JsonApiResponseSerializer
        )
    )
]