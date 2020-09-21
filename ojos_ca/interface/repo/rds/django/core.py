import json
from logging import basicConfig, getLogger, INFO
from typing import Any, Dict, List, Optional, Tuple

from django.db.utils import IntegrityError
from django.db.models.manager import Manager

from ojos_ca.domain.entity.core import Entity
from ojos_ca.usecase.serializer import JsonSerializer
# from ojos_ca.usecase.serializer.django import ModelSerializer

from ...core import DataStoreRepo
from ...exception import DoesNotExistException, DidNotSaveException

from .model import BaseModel

basicConfig()
logger = getLogger(__name__)
logger.setLevel(INFO)


class ModelRepo(DataStoreRepo):
    def __init__(self, model: BaseModel, serializer: JsonSerializer, *args, **kwargs):
        self._model      = model
        self._client     = model.objects
        self._serializer = serializer

    @property
    def serializer(self) -> JsonSerializer:
        return self._serializer

    @property
    def model(self) -> BaseModel:
        return self._model

    def find_all(self, 
        order: Optional[List[str]]=None,
        count: Optional[int]=None, *args, **kwargs) -> List[Entity]:
        qs = self._client.all()
        if order is not None:
            qs = qs.order_by(*order)
        if count is not None:
            qs = qs[:count]
        return [self._serializer.model_to_entity(model) for model in qs]

    def find_by(self,
            conditions: Dict[str, Any],
            order: Optional[List[str]]=None,
            count: Optional[int]=None, *args, **kwargs) -> List[Entity]:
        qs = self._client.filter(**conditions)
        if order is not None:
            qs = qs.order_by(*order)
        if count is not None:
            qs = qs[:count]
        return [self._serializer.model_to_entity(model) for model in qs]

    def count_by(self,
        conditions: Optional[Dict[str, str]]=None, *args, **kwargs) -> int:
        if conditions is None:
            return self._client.all().count()
        else:
            return self._client.filter(**conditions).count()

    def find_by_key(self, key: str, *args, **kwargs) -> Optional[Entity]:
        try:
            model = self._client.get(pk=key)
            return self._serializer.model_to_entity(model)
        except self._model.DoesNotExist:
            return None

    def create(self, entity: Entity, *args, **kwargs) -> None:
        logger.info('This method is an alias of update_or_create')
        self.update_or_create(entity)

    def update(self, entity: Entity, *args, **kwargs) -> None:
        logger.info('This method is an alias of update_or_create')
        self.update_or_create(entity)

    def delete(self, key: str, *args, **kwargs) -> None:
        try:
            model = self._client.get(pk=key)
            model.delete()
        except self._model.DoesNotExist:
            pass

    def delete_by(self,
        conditions=Dict[str, Any], *args, **kwargs) -> None:
        self._client.filter(**conditions).delete()

    def delete_all(self, *args, **kwargs) -> None:
        self._client.all().delete()

    def get_or_create(self, entity: Entity, *args, **kwargs) -> Tuple[Entity, bool]:
        model, created = self._client.get_or_create(
            **self._serializer.entity_to_defaults(entity)
        )
        if not created:
            entity = self._serializer.model_to_entity(model)
        return entity, created

    def update_or_create(self, entity: Entity, *args, **kwargs) -> Tuple[Entity, bool]:
        model, created = self._client.update_or_create(
            **self._serializer.entity_to_defaults(entity)
        )
        entity = self._serializer.model_to_entity(model)
        return entity, created

    def bulk_create(self, entities: List[Entity], batch_size: int=None, *args, **kwargs) -> List[Entity]:
        models = [self._serializer.entity_to_model(entity) for entity in entities]
        return [
            self._serializer.model_to_entity(model) 
            for model in self._client.bulk_create(models, batch_size)
        ]

    def bulk_update(self, entities: List[Entity], fields: List[str], batch_size: int=None, *args, **kwargs) -> None:
        models = [self._serializer.entity_to_model(entity) for entity in entities]
        self._client.bulk_update(models, fields, batch_size)

