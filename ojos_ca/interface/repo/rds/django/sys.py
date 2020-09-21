from typing import Any, Dict, List, Optional, Tuple

from ojos_ca.domain.entity.sys import (
    SysVar, Seq
)

from .core import ModelRepo


class SysVarModelRepo(ModelRepo):
    def find_all(self, 
        order: Optional[List[str]]=None,
        count: Optional[int]=None, *args, **kwargs) -> List[SysVar]:
        return super(SysVarModelRepo, self).find_all(order=order, count=count, *args, **kwargs)

    def find_by(self, 
            conditions: Optional[Dict[str, Any]],
            order: Optional[List[str]]=None,
            count: Optional[int]=None, *args, **kwargs) -> List[SysVar]:
        return super(SysVarModelRepo, self).find_by(conditions, order, count, *args, **kwargs)

    def find_by_key(self, key: str, *args, **kwargs) -> Optional[SysVar]:
        return super(SysVarModelRepo, self).find_by_key(key, *args, **kwargs)

    def create(self, entity: SysVar, *args, **kwargs) -> None:
        super(SysVarModelRepo, self).create(entity, *args, **kwargs)

    def update(self, entity: SysVar, *args, **kwargs) -> None:
        super(SysVarModelRepo, self).update(entity, *args, **kwargs)

    def get_or_create(self, entity: SysVar, *args, **kwargs) -> Tuple[SysVar, bool]:
        return super(SysVarModelRepo, self).get_or_create(entity, *args, **kwargs)

    def update_or_create(self, entity: SysVar, *args, **kwargs) -> Tuple[SysVar, bool]:
        return super(SysVarModelRepo, self).update_or_create(entity, *args, **kwargs)

    def bulk_create(self, entities: List[SysVar], batch_size: int=None, *args, **kwargs) -> List[SysVar]:
        return super(SysVarModelRepo, self).bulk_create(entities, batch_size, *args, **kwargs)

    def bulk_update(self, entities: List[SysVar], fields: List[str], batch_size: int=None, *args, **kwargs) -> None:
        super(SysVarModelRepo, self).bulk_update(entities, fields, batch_size, *args, **kwargs)


class SeqModelRepo(ModelRepo):
    def find_all(self, 
        order: Optional[List[str]]=None,
        count: Optional[int]=None, *args, **kwargs) -> List[Seq]:
        return super(SeqModelRepo, self).find_all(order=order, count=count, *args, **kwargs)

    def find_by(self, 
            conditions: Optional[Dict[str, Any]],
            order: Optional[List[str]]=None,
            count: Optional[int]=None, *args, **kwargs) -> List[Seq]:
        return super(SeqModelRepo, self).find_by(conditions, order, count, *args, **kwargs)

    def find_by_key(self, key: str, *args, **kwargs) -> Optional[Seq]:
        return super(SeqModelRepo, self).find_by_key(key, *args, **kwargs)

    def create(self, entity: Seq, *args, **kwargs) -> None:
        super(SeqModelRepo, self).create(entity, *args, **kwargs)

    def update(self, entity: Seq, *args, **kwargs) -> None:
        super(SeqModelRepo, self).update(entity, *args, **kwargs)

    def get_or_create(self, entity: Seq, *args, **kwargs) -> Tuple[Seq, bool]:
        return super(SeqModelRepo, self).get_or_create(entity, *args, **kwargs)

    def update_or_create(self, entity: Seq, *args, **kwargs) -> Tuple[Seq, bool]:
        return super(SeqModelRepo, self).update_or_create(entity, *args, **kwargs)

    def bulk_create(self, entities: List[Seq], batch_size: int=None, *args, **kwargs) -> List[Seq]:
        return super(SeqModelRepo, self).bulk_create(entities, batch_size, *args, **kwargs)

    def bulk_update(self, entities: List[Seq], fields: List[str], batch_size: int=None, *args, **kwargs) -> None:
        super(SeqModelRepo, self).bulk_update(entities, fields, batch_size, *args, **kwargs)