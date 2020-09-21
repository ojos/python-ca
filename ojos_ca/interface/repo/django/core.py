from typing import List

from ojos_ca.domain.entity import Entity
from ojos_ca.usecase.serializer.django import ModelSerializer

from .. import RdbKvsRepo


class ModelRedisRepo(RdbKvsRepo):
    @property
    def serializer(self) -> ModelSerializer:
        return self._serializer

    def bulk_create(self, entities: List[Entity], batch_size: int=None, *args, **kwargs) -> List[Entity]:
        entities = self.rds_repo.bulk_create(entities, batch_size, *args, **kwargs)
        self.kvs_repo.bulk_create(entities, *args, **kwargs)
        return entities

    def bulk_update(self, entities: List[Entity], fields: List[str], batch_size: int=None, *args, **kwargs) -> None:
        self.rds_repo.bulk_update(entities, fields, batch_size, *args, **kwargs)
        self.kvs_repo.bulk_update(entities, *args, **kwargs)
