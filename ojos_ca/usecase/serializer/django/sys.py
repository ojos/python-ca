from datetime import datetime
from typing import Any, List, Optional

from ojos_ca.domain.entity.sys import SysVar, Seq
from ojos_ca.interface.repo.rds.django.model.sys import (
    SysVarModel, SeqModel
)

from ..sys import SeqJsonSerializer, SysVarJsonSerializer
from .core import ModelSerializer


class SeqModelSerializer(SeqJsonSerializer, ModelSerializer):
    @classmethod
    def model_to_entity(cls, model:SeqModel) -> Seq:
        return Seq(
            seq_id=model.seq_id,
            count=model.count,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @classmethod
    def entity_to_model(cls, entity: Seq) -> SeqModel:
        return SeqModel(
            seq_id=entity.seq_id,
            count=entity.count,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @classmethod
    def model_to_dict(cls, model:SysVarModel, ignore_keys: List[Any]=[]) -> dict:
        return super(SeqModelSerializer, cls).model_to_dict(model, ignore_keys)

    @classmethod
    def dict_to_model(cls, **kwargs) -> SeqModel:
        return super(SeqModelSerializer, cls).dict_to_model(**kwargs)


class SysVarModelSerializer(SysVarJsonSerializer, ModelSerializer):
    @classmethod
    def model_to_entity(cls, model:SysVarModel) -> SysVar:
        return SysVar(
            key=model.key,
            raw_data=model.raw_data,
            module=model.module,
            note=model.note,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @classmethod
    def entity_to_model(cls, entity: SysVar) -> SysVarModel:
        return SysVarModel(
            key=entity.key,
            raw_data=entity.raw_data,
            module=entity.module,
            note=entity.note,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @classmethod
    def model_to_dict(cls, model:SysVarModel, ignore_keys: List[Any]=[]) -> dict:
        return super(SysVarModelSerializer, cls).model_to_dict(model, ignore_keys)

    @classmethod
    def dict_to_model(cls, **kwargs) -> SysVarModel:
        return super(SysVarModelSerializer, cls).dict_to_model(**kwargs)
