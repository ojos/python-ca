from typing import Any, List, Tuple

from ojos_ca.domain.entity import Entity
from ojos_ca.interface.repo.rds.django.model import BaseModel

from ..core import JsonSerializer

class ModelSerializer(JsonSerializer):

    @classmethod
    def model_to_entity(cls, model:BaseModel) -> Entity:
        raise NotImplementedError('Not Implemented {}'.format(cls.__name__))

    @classmethod
    def entity_to_model(cls, entity: Entity) -> Tuple[BaseModel, ...]:
        raise NotImplementedError('Not Implemented {}'.format(cls.__name__))

    @classmethod
    def model_to_dict(cls, model:BaseModel, ignore_keys: List[Any]) -> dict:
        return cls.entity_to_dict(cls.model_to_entity(model), ignore_keys)

    @classmethod
    def dict_to_model(cls, **kwargs) -> Tuple[BaseModel, ...]:
        return cls.entity_to_model(cls.dict_to_entity(**kwargs))

    @classmethod
    def entity_to_defaults(cls, entity: Entity) -> dict:
        defaults = cls.entity_to_dict(entity, ignore_keys=[entity.pk])
        return {'pk': getattr(entity, entity.pk), 'defaults': defaults}
