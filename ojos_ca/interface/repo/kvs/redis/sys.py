from typing import Any, Dict, List, Optional, Tuple

from ojos_ca.domain.entity.sys import Seq, SysVar

from .core import RedisStringRepo


class SysVarRedisRepo(RedisStringRepo):
    KEY_NAME           = 'app/sys_var/{}'
    CACHE_TIMEOUT      = 5 * 60

    def find_all(self, 
        order: Optional[List[str]]=None,
        count: Optional[int]=None) -> List[SysVar]:
        return super(SysVarRedisRepo, self).find_all(order=order, count=count)

    def find_by(self, 
            conditions: Dict[str, Any],
            order: Optional[List[str]]=None,
            count: Optional[int]=None) -> List[SysVar]:
        return super(SysVarRedisRepo, self).find_by(conditions, order, count)

    def find_by_key(self, key: str) -> Optional[SysVar]:
        return super(SysVarRedisRepo, self).find_by_key(key)

    def get_or_create(self, entity: SysVar) -> Tuple[SysVar, bool]:
        return super(SysVarRedisRepo, self).get_or_create(entity)

    def update_or_create(self, entity: SysVar) -> Tuple[SysVar, bool]:
        return super(SysVarRedisRepo, self).update_or_create(entity)

    def bulk_update(self, entities: List[SysVar], *args, **kwargs) -> None:
        return super(SysVarRedisRepo, self).bulk_update(entities)

class SeqRedisRepo(RedisStringRepo):
    KEY_NAME           = 'app/seq/{}'
    CACHE_TIMEOUT      = 0

    def find_all(self, 
        order: Optional[List[str]]=None,
        count: Optional[int]=None) -> List[Seq]:
        return super(SeqRedisRepo, self).find_all(order=order, count=count)

    def find_by(self, 
            conditions: Dict[str, Any],
            order: Optional[List[str]]=None,
            count: Optional[int]=None) -> List[Seq]:
        return super(SeqRedisRepo, self).find_by(conditions, order, count)

    def find_by_key(self, key: str) -> Optional[Seq]:
        return super(SeqRedisRepo, self).find_by_key(key)

    def get_or_create(self, entity: Seq) -> Tuple[Seq, bool]:
        return super(SeqRedisRepo, self).get_or_create(entity)

    def update_or_create(self, entity: Seq) -> Tuple[Seq, bool]:
        return super(SeqRedisRepo, self).update_or_create(entity)

    def bulk_update(self, entities: List[Seq], *args, **kwargs) -> None:
        return super(SeqRedisRepo, self).bulk_update(entities)
