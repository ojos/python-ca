from typing import Any, Dict, List, Optional, Tuple

from ojos_ca.domain.entity.sys import Seq, SysVar
from ojos_ca.usecase.serializer.django.sys import(
    SeqModelSerializer, SysVarModelSerializer
)

from .core import ModelRedisRepo
from ..rds.django import SeqModelRepo, SysVarModelRepo
from ..kvs.redis import SeqRedisRepo, SysVarRedisRepo


class SeqRepo(ModelRedisRepo):
    def __init__(self,
            rds_repo: SeqModelRepo,
            kvs_repo: SeqRedisRepo,
            serializer: SeqModelSerializer):
        super(SeqRepo, self).__init__(rds_repo, kvs_repo, serializer)

    def find_all(self,
            order: Optional[List[str]]=None,
            count: Optional[int]=None,
            cache: bool=True) -> List[Seq]:
        return super(SeqRepo, self).find_all(order=order, count=count, cache=cache)

    def find_by(self,
            conditions: Optional[Dict[str, Any]],
            order: Optional[List[str]]=None,
            count: Optional[int]=None,
            cache: bool=True) -> List[Seq]:
        return super(SeqRepo, self).find_by(conditions, order, count, cache)

    def find_by_key(self, key: str, cache: bool=True) -> Optional[Seq]:
        return super(SeqRepo, self).find_by_key(key, cache)

    def create(self, entity: Seq) -> None:
        super(SeqRepo, self).create(entity)

    def update(self, entity: Seq) -> None:
        super(SeqRepo, self).update(entity)

    def get_or_create(self, entity: Seq, cache: bool=False) -> Tuple[Seq, bool, bool]:
        return super(SeqRepo, self).get_or_create(entity, cache)

    def update_or_create(self, entity: Seq) -> Tuple[Seq, bool, bool]:
        return super(SeqRepo, self).update_or_create(entity)

    def bulk_create(self, entities: List[Seq], batch_size: int=None, *args, **kwargs) -> List[Seq]:
        return super(SeqRepo, self).bulk_create(entities, batch_size, *args, **kwargs)

    def bulk_update(self, entities: List[Seq], fields: List[str], batch_size: int=None, *args, **kwargs) -> None:
        super(SeqRepo, self).bulk_update(entities, fields, batch_size, *args, **kwargs)


class SysVarRepo(ModelRedisRepo):
    def __init__(self, 
            rds_repo: SysVarModelRepo,
            kvs_repo: SysVarRedisRepo,
            serializer: SysVarModelSerializer):
        super(SysVarRepo, self).__init__(rds_repo, kvs_repo, serializer)

    def find_all(self,
            order: Optional[List[str]]=None,
            count: Optional[int]=None,
            cache: bool=True) -> List[SysVar]:
        return super(SysVarRepo, self).find_all(order=order, count=count, cache=cache)

    def find_by(self,
            conditions: Optional[Dict[str, Any]],
            order: Optional[List[str]]=None,
            count: Optional[int]=None,
            cache: bool=True) -> List[SysVar]:
        return super(SysVarRepo, self).find_by(conditions, order, count, cache)

    def find_by_key(self, key: str, cache: bool=True) -> Optional[SysVar]:
        return super(SysVarRepo, self).find_by_key(key, cache)

    def create(self, entity: SysVar) -> None:
        super(SysVarRepo, self).create(entity)

    def update(self, entity: SysVar) -> None:
        super(SysVarRepo, self).update(entity)

    def get_or_create(self, entity: SysVar, cache: bool=False) -> Tuple[SysVar, bool, bool]:
        return super(SysVarRepo, self).get_or_create(entity, cache)

    def update_or_create(self, entity: SysVar) -> Tuple[SysVar, bool, bool]:
        return super(SysVarRepo, self).update_or_create(entity)

    def bulk_create(self, entities: List[SysVar], batch_size: int=None, *args, **kwargs) -> List[SysVar]:
        return super(SysVarRepo, self).bulk_create(entities, batch_size, *args, **kwargs)

    def bulk_update(self, entities: List[SysVar], fields: List[str], batch_size: int=None, *args, **kwargs) -> None:
        super(SysVarRepo, self).bulk_update(entities, fields, batch_size, *args, **kwargs)