from datetime import datetime
from typing import Optional

from ojos.sys import lazy_loader

from ojos_ca.domain.value_object.sys import (
    SeqId, SeqCount,
    SysVarKey, SysVarRawData, SysVarModule, SysVarNote,
)

from ojos_ca.domain.entity.core import DatetimeEntity


class Seq(DatetimeEntity):
    def __init__(self,
            seq_id: str,
            count: int,
            created_at: Optional[datetime]=None,
            updated_at: Optional[datetime]=None, *args, **kwargs):
        self.seq_id = seq_id
        self.count      = count
        super(Seq, self).__init__(created_at, updated_at)

    @property
    def pk(self):
        return 'seq_id'

    @property
    def map(self):
        return {
            'seq_id':     self.seq_id,
            'count':      self.count,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @property
    def seq_id(self) -> str:
        return self._seq_id.value

    @seq_id.setter
    def seq_id(self, value: str):
        self._seq_id = SeqId(value)

    @property
    def count(self) -> str:
        return self._count.value

    @count.setter
    def count(self, value: str):
        self._count = SeqCount(value)


class SysVar(DatetimeEntity):
    def __init__(self,
            key: str,
            raw_data: str,
            module: str=SysVarModule.DEFAULT_VALUE,
            note: str='',
            created_at: Optional[datetime]=None,
            updated_at: Optional[datetime]=None, *args, **kwargs):
        self.key      = key
        self.raw_data = raw_data
        self.module   = module
        self.note     = note
        super(SysVar, self).__init__(created_at, updated_at)

    def __it__(self, other):
        return self.key < other.key

    @property
    def pk(self):
        return 'key'

    @property
    def map(self):
        return {
            'key':        self.key,
            'raw_data':   self.raw_data,
            'module':     self.module,
            'note':       self.note,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @property
    def value(self):
        try:
            _module = eval(self.module)
        except:
            _module = lazy_loader(self.module)
        return _module(self.raw_data)

    @property
    def key(self) -> str:
        return self._key.value

    @key.setter
    def key(self, value: str):
        self._key = SysVarKey(value)

    @property
    def raw_data(self) -> str:
        return self._raw_data.value

    @raw_data.setter
    def raw_data(self, value: str):
        self._raw_data = SysVarRawData(value)

    @property
    def module(self) -> str:
        return self._module.value

    @module.setter
    def module(self, value: str):
        self._module = SysVarModule(value)

    @property
    def note(self) -> str:
        return self._note.value

    @note.setter
    def note(self, value: str):
        self._note = SysVarNote(value)