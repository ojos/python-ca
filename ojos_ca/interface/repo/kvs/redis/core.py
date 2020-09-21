import json
from logging import basicConfig, getLogger, INFO
from operator import attrgetter
from redis import StrictRedis
from typing import Any, Dict, List, NoReturn, Optional, Tuple


from ojos_ca.domain.entity import Entity
from ojos_ca.usecase.serializer import JsonSerializer

from ...core import DataStoreRepo
from ...exception import DidNotSaveException


basicConfig()
logger = getLogger(__name__)
logger.setLevel(INFO)


class RedisRepo(DataStoreRepo):
    CACHE_TIMEOUT      = 5 * 60

    def __init__(self, client: StrictRedis, serializer: JsonSerializer, *args, **kwargs):
        self._client     = client
        self._serializer = serializer

    def _order_by(self, entities: List[Entity], order: Optional[List[str]]=None) -> List[Entity]:
        _entities = entities
        for key in order:
            if key[0] == '-':
                _entities = sorted(_entities, key=attrgetter(key[1:]), reverse=True)
            else:
                _entities = sorted(_entities, key=attrgetter(key))
        return _entities

    # conditionsはandの絞り込みのみ
    def find_by(self,
            conditions: Dict[str, Any],
            order: Optional[List[str]]=None,
            count: Optional[int]=None) -> List[Entity]:
        entities = self.find_all(order=order, count=count)
        for key, val in conditions.items():
            entities = [e for e in entities if getattr(e, key) == val]
        if count is not None:
            entities = entities[:count]
        return entities

    def create(self, entity: Entity) -> None:
        logger.info('This method is an alias of update_or_create')
        self.update_or_create(entity)

    def update(self, entity: Entity) -> None:
        logger.info('This method is an alias of update_or_create')
        self.update_or_create(entity)

    def bulk_create(self, entities: List[Entity], *args, **kwargs) -> None:
        logger.info('This method is an alias of bulk_update')
        self.bulk_update(entities)

class RedisStringRepo(RedisRepo):
    KEY_NAME = 'app/key_name/{}'

    def _find_all_cache_key(self) -> List[str]:
        return self._client.keys(pattern=self.KEY_NAME.format('*'))

    def find_all(self, 
        order: Optional[List[str]]=None,
        count: Optional[int]=None) -> List[Entity]:
        entities = [
            self._serializer.dict_to_entity(**self._serializer.json_to_dict(json_str)) 
            for json_str in filter(None, self._client.mget(self._find_all_cache_key()))
        ]
        if order is not None:
            entities = self._order_by(entities, order)
        if count is not None:
            entities = entities[:count]
        return entities

    def find_by_key(self, key: str) -> Optional[Entity]:
        json_str = self._client.get(name=self.KEY_NAME.format(key))
        if json_str is None:
            return None
        return self._serializer.dict_to_entity(**self._serializer.json_to_dict(json_str))

    def count_by(self, conditions: Optional[Dict[str, str]]=None) -> int:
        if conditions is None:
            return len(self.find_all())
        else:
            return len(self.find_by(conditions))

    def delete(self, key: str) -> NoReturn:
        self._client.delete(self.KEY_NAME.format(key))

    def delete_by(self, conditions=Dict[str, Any]) -> NoReturn:
        for entity in self.find_by(conditions):
            self._client.delete(self.KEY_NAME.format(getattr(entity, entity.pk)))

    def delete_all(self) -> NoReturn:
        [
            self.delete(key.decode().split('/')[-1])
            for key in self._find_all_cache_key()
        ]

    def get_or_create(self, entity: Entity) -> Tuple[Entity, bool]:
        _entity = self.find_by_key(entity.pk)
        created = False
        if _entity is None:
            _entity, created = self.update_or_create(entity)
        return _entity, created

    def update_or_create(self, entity: Entity) -> Tuple[Entity, bool]:
        json_str = self._serializer.dict_to_json(self._serializer.entity_to_dict(entity))
        key_name = self.KEY_NAME.format(getattr(entity, entity.pk))
        try:
            if self.CACHE_TIMEOUT > 0:
                created = self._client.setex(
                    name=key_name,
                    time=self.CACHE_TIMEOUT,
                    value=json_str
                )
            else:
                created = self._client.set(
                    name=key_name,
                    value=json_str
                )
        except:
            raise DidNotSaveException(name=self.__class__.__name__, value=key_name)
        return entity, bool(created)

    def bulk_update(self, entities: List[Entity], *args, **kwargs) -> None:
        json_dicts = {
            self.KEY_NAME.format(getattr(entity, entity.pk)): self._serializer.dict_to_json(self._serializer.entity_to_dict(entity))
            for entity in entities
        }
        self._client.mset(json_dicts)

        if self.CACHE_TIMEOUT > 0:
            pipe = self._client.pipeline()
            for key in json_dicts.keys():
                pipe.expire(key, self.CACHE_TIMEOUT)
            pipe.execute()


class RedisHashRepo(RedisRepo):
    HASH_KEY_NAME = 'app/hash_key_name'

    def find_all(self, 
        order: Optional[List[str]]=None,
        count: Optional[int]=None) -> List[Entity]:
        entities = [
            self._serializer.dict_to_entity(**self._serializer.json_to_dict(json_str))
            for json_str in self._client.hgetall(self.HASH_KEY_NAME).values()
        ]
        if order is not None:
            entities = self._order_by(entities, order)
        if count is not None:
            entities = entities[:count]
        return entities

    def find_by_key(self, key: str) -> Optional[Entity]:
        json_str = self._client.hget(self.HASH_KEY_NAME, key)
        if json_str is None:
            return None
        return self._serializer.dict_to_entity(**self._serializer.json_to_dict(json_str))

    def count_by(self, conditions: Optional[Dict[str, str]]=None) -> int:
        if conditions is None:
            return self._client.hlen(self.HASH_KEY_NAME)
        else:
            return len(self.find_by(conditions))

    def delete(self, key: str) -> NoReturn:
        self._client.hdel(self.HASH_KEY_NAME, key)

    def delete_by(self, conditions=Dict[str, Any]) -> NoReturn:
        for entity in self.find_by(conditions):
            self._client.delete(getattr(entity, entity.pk))

    def delete_all(self) -> NoReturn:
        self._client.delete(self.HASH_KEY_NAME)

    def get_or_create(self, entity: Entity) -> Tuple[Entity, bool]:
        _entity = self.find_by_key(entity.pk)
        created = False
        if _entity is None:
            _entity, created = self.update_or_create(entity)
        return _entity, created

    def update_or_create(self, entity: Entity) -> Tuple[Entity, bool]:
        json_str = self._serializer.dict_to_json(self._serializer.entity_to_dict(entity))
        key = getattr(entity, entity.pk)
        try:
            created = self._client.hset(name=self.HASH_KEY_NAME,
                                        key=key,
                                        value=json_str)
            if self.CACHE_TIMEOUT > 0:
                self._client.expire(self.HASH_KEY_NAME, self.CACHE_TIMEOUT)
        except:
            raise DidNotSaveException(name=self.__class__.__name__, value=key)
        return entity, bool(created)

    def bulk_update(self, entities: List[Entity], *args, **kwargs) -> None:
        json_dicts = {
            getattr(entity, entity.pk): self._serializer.dict_to_json(self._serializer.entity_to_dict(entity))
            for entity in entities
        }
        self._client.hmset(name=self.HASH_KEY_NAME, mapping=json_dicts)

        if self.CACHE_TIMEOUT > 0:
                self._client.expire(self.HASH_KEY_NAME, self.CACHE_TIMEOUT)
