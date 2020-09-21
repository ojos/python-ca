import json
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Optional

from ojos.conv.json import serialize
from ojos_ca.domain.value_object import DatetimeRange


class Entity(object, metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        pass

    def __str__(self):
        return '{}'.format(json.dumps(
            self.map, 
            ensure_ascii=False,
            default=serialize))

    def __repr__(self):
        return '<{}({})>'.format(self.__class__.__name__, self.map)

    @property
    @abstractmethod
    def pk(self):
        raise NotImplementedError('Not Implemented {}: {}'.format(self.__class__.__name__, 'pk'))

    @property
    @abstractmethod
    def map(self):
        raise NotImplementedError('Not Implemented {}: {}'.format(self.__class__.__name__, 'map'))

class DatetimeEntity(Entity):
    def __init__(self, 
            created_at: Optional[datetime]=None,
            updated_at: Optional[datetime]=None, *args, **kwargs):
        self.created_at = created_at
        self.updated_at = updated_at

    def __it__(self, other):
        return self.created_at < other.created_at

    # @property
    # def map(self):
    #     return {'created_at': self.created_at,
    #             'updated_at': self.updated_at}

    @property
    def created_at(self) -> Optional[datetime]:
        return self._created_at.value

    @created_at.setter
    def created_at(self, value: datetime):
        self._created_at = DatetimeRange(value, allow_none=True)

    @property
    def updated_at(self) -> Optional[datetime]:
        return self._updated_at.value

    @updated_at.setter
    def updated_at(self, value: datetime):
        self._updated_at = DatetimeRange(value, allow_none=True)


