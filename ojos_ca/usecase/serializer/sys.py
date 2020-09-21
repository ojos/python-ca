from datetime import datetime
from typing import Any, List, Optional


from ojos_ca.domain.entity.sys import SysVar, Seq
from ojos_ca.domain.value_object.sys import SysVarModule

from .core import JsonSerializer


class SeqJsonSerializer(JsonSerializer):
    @classmethod
    def dict_to_entity(cls,
            seq_id: str,
            count: int,
            created_at: Optional[datetime]=None,
            updated_at: Optional[datetime]=None, **kwargs) -> Seq:
        return Seq(
            seq_id=seq_id,
            count=count,
            created_at=created_at,
            updated_at=updated_at
        )


class SysVarJsonSerializer(JsonSerializer):
    @classmethod
    def dict_to_entity(cls,
            key: str,
            raw_data: str,
            module: str=SysVarModule.DEFAULT_VALUE,
            note: str='',
            created_at: Optional[datetime]=None,
            updated_at: Optional[datetime]=None, **kwargs) -> SysVar:
        return SysVar(
            key=key,
            raw_data=raw_data,
            module=module,
            note=note,
            created_at=created_at,
            updated_at=updated_at
        )
