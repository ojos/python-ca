from ojos_ca.interface.repo.rds.django.model import (
    SeqModel, SysVarModel
)
from ojos_ca.interface.repo.rds.django import (
    SeqModelRepo, SysVarModelRepo
)
from ojos_ca.usecase.serializer.django.sys import (
    SeqModelSerializer, SysVarModelSerializer
)

class SeqModelRepoFactory(object):
    @staticmethod
    def get() -> SeqModelRepo:
        return SeqModelRepo(SeqModel, SeqModelSerializer)


class SysVarModelRepoFactory(object):
    @staticmethod
    def get() -> SysVarModelRepo:
        return SysVarModelRepo(SysVarModel, SysVarModelSerializer)
