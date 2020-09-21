import json
import re
from datetime import datetime
from typing import Any, List, Optional, Union

from logging import basicConfig, getLogger, INFO

from ojos.conv.datetime import dt_to_int, int_to_dt, ISO_FORMAT_PATTERN

from ojos_ca.domain.entity import Entity

basicConfig()
logger = getLogger(__name__)
logger.setLevel(INFO)


class JsonSerializer(object):
    DATERIME_DIST = str

    @classmethod
    def json_to_dict(cls, json_str: str) -> dict:
        def _load_to_dt(obj):
            for (key, value) in obj.items():
                if isinstance(value, int) and (value > dt_to_int(datetime(2019,7,1,0,0,0), microsecond=True)):
                    obj[key] = int_to_dt(value, microsecond=True)
                elif isinstance(value, str) and re.match(ISO_FORMAT_PATTERN, value):
                    obj[key] = datetime.fromisoformat(value)
            return obj
        return json.loads(json_str, object_hook=_load_to_dt)

    @classmethod
    def dict_to_json(cls, 
            obj: dict, 
            ensure_ascii: bool=False,
            indent: Optional[int]=None,
            dt_dist: Union[str, int]=str) -> str:
        def _datetime_to_str(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError('Object of type {} is not JSON serializable'.format(type(obj)))

        def _datetime_to_int(obj):
            if isinstance(obj, datetime):
                return dt_to_int(obj, microsecond=True)
            raise TypeError('Object of type {} is not JSON serializable'.format(type(obj)))

        _default = _datetime_to_int if dt_dist == int else _datetime_to_str
        return json.dumps(obj, ensure_ascii=ensure_ascii, indent=indent, default=_default)

    @classmethod
    def entity_to_dict(cls, entity: Entity, ignore_keys: List[Any]=[]) -> dict:
        map = entity.map
        for key in ignore_keys:
            map.pop(key)
        return map

    @classmethod
    def dict_to_entity(cls, **kwargs) -> Entity:
        raise NotImplementedError('Not Implemented {}'.format(cls.__name__))

