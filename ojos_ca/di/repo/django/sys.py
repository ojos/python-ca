from django.conf import settings

from ojos_ca.interface.repo.django import (
    SeqRepo, SysVarRepo
)
from ojos_ca.usecase.serializer.django.sys import(
    SeqModelSerializer, SysVarModelSerializer
)

from ..kvs.redis import (
    SeqRedisRepoFactory, SysVarRedisRepoFactory
)
from ..rds.django import (
    SeqModelRepoFactory, SysVarModelRepoFactory
)


class SeqRepoFactory(object):
    @staticmethod
    def get() -> SeqRepo:
        rds_repo = SeqModelRepoFactory.get()
        kvs_repo = SeqRedisRepoFactory.get(host=settings.CACHE_HOST)
        return SeqRepo(rds_repo, kvs_repo, SeqModelSerializer)


class SysVarRepoFactory(object):
    @staticmethod
    def get() -> SysVarRepo:
        rds_repo = SysVarModelRepoFactory.get()
        kvs_repo = SysVarRedisRepoFactory.get(host=settings.CACHE_HOST)
        return SysVarRepo(rds_repo, kvs_repo, SysVarModelSerializer)

