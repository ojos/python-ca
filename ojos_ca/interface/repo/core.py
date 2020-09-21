from abc import ABCMeta, abstractmethod
from logging import basicConfig, getLogger, INFO
from typing import Any, Counter, Dict, List, Optional, Tuple

from ojos_ca.domain.entity.core import Entity
from ojos_ca.usecase.serializer import JsonSerializer

basicConfig()
logger = getLogger(__name__)
logger.setLevel(INFO)


class DataStoreRepo(object):
    def __init__(self, client: Any, serializer: JsonSerializer, *args, **kwargs):
        self._client     = client
        self._serializer = serializer

    @property
    def serializer(self) -> JsonSerializer:
        return self._serializer

    def find_all(self,
        order: Optional[List[str]]=None,
        count: Optional[int]=None, *args, **kwargs) -> List[Entity]:
        logger.warn('Not Implemented {}: {}'.format(self.__class__.__name__, 'find_all'))
        return []

    def find_by(self,
            conditions: Dict[str, Any],
            order: Optional[List[str]]=None,
            count: Optional[int]=None, *args, **kwargs) -> List[Entity]:
        logger.warn('Not Implemented {}: {}'.format(self.__class__.__name__, 'find_by'))

    def count_by(self, conditions: Optional[Dict[str, str]]=None, *args, **kwargs) -> int:
        logger.warn('Not Implemented {}: {}'.format(self.__class__.__name__, 'count_by'))

    def find_by_key(self, key: str, *args, **kwargs) -> Optional[Entity]:
        logger.warn('Not Implemented {}: {}'.format(self.__class__.__name__, 'find_by_key'))

    def create(self, entity: Entity, *args, **kwargs) -> None:
        logger.warn('Not Implemented {}: {}'.format(self.__class__.__name__, 'create'))

    def update(self, entity: Entity, *args, **kwargs) -> None:
        logger.warn('Not Implemented {}: {}'.format(self.__class__.__name__, 'update'))

    def delete(self, key: str, *args, **kwargs) -> None:
        logger.warn('Not Implemented {}: {}'.format(self.__class__.__name__, 'delete'))

    def delete_by(self, conditions: Optional[Dict[str, Any]]=None, *args, **kwargs) -> None:
        logger.warn('Not Implemented {}: {}'.format(self.__class__.__name__, 'delete_by'))

    def delete_all(self, *args, **kwargs) -> None:
        logger.warn('Not Implemented {}: {}'.format(self.__class__.__name__, 'delete_all'))

    def get_or_create(self, entity: Entity, *args, **kwargs) -> Tuple[Entity, bool]:
        logger.warn('Not Implemented {}: {}'.format(self.__class__.__name__, 'get_or_create'))

    def update_or_create(self, entity: Entity, *args, **kwargs) -> Tuple[Entity, bool]:
        logger.warn('Not Implemented {}: {}'.format(self.__class__.__name__, 'update_or_create'))

    def bulk_create(self, entities: List[Entity], *args, **kwargs) -> List[Entity]:
        logger.warn('Not Implemented {}: {}'.format(self.__class__.__name__, 'bulk_create'))

    def bulk_update(self, entities: List[Entity], *args, **kwargs) -> None:
        logger.warn('Not Implemented {}: {}'.format(self.__class__.__name__, 'bulk_update'))


class RdbKvsRepo(DataStoreRepo):
    def __init__(self, 
            rds_repo: DataStoreRepo,
            kvs_repo: DataStoreRepo,
            serializer: Any, *args, **kwargs):
        self._rds_repo = rds_repo
        self._kvs_repo = kvs_repo
        self._serializer = serializer

    @property
    def rds_repo(self) -> DataStoreRepo:
        return self._rds_repo

    @property
    def kvs_repo(self) -> DataStoreRepo:
        return self._kvs_repo

    def find_all(self, 
            order: Optional[List[str]]=None,
            count: Optional[int]=None,
            cache: bool=True, *args, **kwargs) -> List[Entity]:
        entities = self.kvs_repo.find_all(order=order, count=count) if cache else []
        if len(entities) != self.rds_repo.count_by():
            entities = self.rds_repo.find_all(order=order, count=count)
            if len(entities) > 0:
                for entity in entities:
                    self.kvs_repo.update_or_create(entity)
        return entities

    def find_by(self, 
            conditions: Dict[str, Any],
            order: Optional[List[str]]=None,
            count: Optional[int]=None,
            cache: bool=True, *args, **kwargs) -> List[Entity]:
        entities = self.kvs_repo.find_by(conditions, order, count) if cache else []
        if len(entities) == 0:
            entities = self.rds_repo.find_by(conditions, order, count)
            if len(entities) > 0:
                for entity in entities:
                    self.kvs_repo.update_or_create(entity)
        return entities

    def count_by(self, 
            conditions: Optional[Dict[str, str]]=None,
            cache: bool=True, *args, **kwargs) -> int:
        count = self.kvs_repo.count_by(conditions) if cache else 0
        if count == 0:
            count = self.rds_repo.count_by(conditions)
        return count

    def find_by_key(self, key: str, cache=True, *args, **kwargs) -> Optional[Entity]:
        entity = self.kvs_repo.find_by_key(key) if cache else None
        if entity is None:
            entity = self.rds_repo.find_by_key(key)
            if entity is not None:
                self.kvs_repo.update_or_create(entity)
        return entity

    def create(self, entity: Entity, cache: bool=True, *args, **kwargs) -> None:
        logger.info('This method is an alias of update_or_create')
        self.update_or_create(entity)

    def update(self, entity: Entity, cache: bool=True, *args, **kwargs) -> None:
        logger.info('This method is an alias of update_or_create')
        self.update_or_create(entity)

    def delete(self, key: str, cache_only: bool=False, *args, **kwargs) -> None:
        self.kvs_repo.delete(key)
        if not cache_only:
            self.rds_repo.delete(key)

    def delete_by(self, conditions=Dict[str, Any],
                        cache_only: bool=False, *args, **kwargs) -> None:
        self.kvs_repo.delete_by(conditions)
        if not cache_only:
            self.rds_repo.delete_by(conditions)

    def delete_all(self, cache_only: bool=True, *args, **kwargs) -> None:
        self.kvs_repo.delete_all()
        if not cache_only:
            self.rds_repo.delete_all()

    def get_or_create(self, entity: Entity, cache: bool=False) -> Tuple[Entity, bool, bool]:
        if cache:
            entity, cache_created = self.kvs_repo.get_or_create(entity)
            entity, db_created = self.rds_repo.update_or_create(entity)
        else:
            entity, db_created = self.rds_repo.get_or_create(entity)
            entity, cache_created = self.kvs_repo.update_or_create(entity)
        return entity, db_created, cache_created

    def update_or_create(self, entity: Entity) -> Tuple[Entity, bool, bool]:
        entity, db_created = self.rds_repo.update_or_create(entity)
        entity, cache_created = self.kvs_repo.update_or_create(entity)
        return entity, db_created, cache_created

    def bulk_create(self, entities: List[Entity], *args, **kwargs) -> List[Entity]:
        entities = self.rds_repo.bulk_create(entities, *args, **kwargs)
        self.kvs_repo.bulk_create(entities, *args, **kwargs)
        return entities

    def bulk_update(self, entities: List[Entity], *args, **kwargs) -> None:
        self.rds_repo.bulk_update(entities, *args, **kwargs)
        self.kvs_repo.bulk_update(entities, *args, **kwargs)

    

# class IRepo(metaclass=ABCMeta):
#     @abstractmethod
#     def __init__(self, client: Any, serializer: Any, *args, **kwargs):
#         pass

#     @abstractmethod
#     def find_all(self, order: Optional[List[str]]=None) -> List[Entity]:
#         pass

#     @abstractmethod
#     def find_by(self,
#             conditions: Dict[str, Any],
#             order: Optional[List[str]]=None,
#             count: Optional[int]=None) -> List[Entity]:
#         pass

#     @abstractmethod
#     def count_by(self, conditions: Optional[Dict[str, str]]=None) -> int:
#         pass

#     @abstractmethod
#     def find_by_key(self, key: str) -> Optional[Entity]:
#         pass

#     @abstractmethod
#     def create(self, entity: Entity) -> None:
#         pass

#     @abstractmethod
#     def update(self, entity: Entity) -> None:
#         pass

#     @abstractmethod
#     def delete(self, key: str) -> None:
#         pass

#     @abstractmethod
#     def delete_by(self, conditions: Optional[Dict[str, Any]]=None) -> None:
#         pass

#     @abstractmethod
#     def delete_all(self) -> None:
#         pass

#     @abstractmethod
#     def get_or_create(self, entity: Entity) -> Tuple[Entity, bool]:
#         pass

#     @abstractmethod
#     def update_or_create(self, entity: Entity) -> Tuple[Entity, bool]:
#         pass