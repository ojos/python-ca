import csv
import json
import re
import uuid
from typing import Any, Optional, Union
from types import FunctionType

from ojos_ca.domain.value_object.core import IsInstance, Length


class RegExpMatch(IsInstance):
    CLASS_INFO = str
    PATTERN    = r'^.*$'

    def __init__(self,
            value: Any,
            allow_none: Optional[bool]=None,
            class_info: Any=None,
            pattern: Optional[str]=None):
        self._pattern = self.PATTERN if pattern is None else pattern
        super(RegExpMatch, self).__init__(value, allow_none, class_info)

    def __repr__(self):
        return "<{}('{}')>".format(self.__class__.__name__, self.value)

    def conditions(self, value: Any) -> bool:
        return (self._allow_none and value is None) or\
            (isinstance(value, self._class_info) and re.match(self._pattern, value))

class Uuid4Hex(RegExpMatch):
    CLASS_INFO    = str
    PATTERN       = r'^[a-f0-9]{32}$'

    @property
    def uuid_hex(self) -> str:
        return uuid.uuid4().hex

    def __init__(self,
            value: Any = None,
            allow_none: Optional[bool]=None,
            class_info: Any=None,
            pattern: Optional[str]=None):
        value = self.uuid_hex if value is None else value
        super(Uuid4Hex, self).__init__(value, allow_none, class_info, pattern)

class Json(Length):
    CLASS_INFO = (str, bytes)
    MIN        = 2

    @property
    def dict(self):
        return json.loads(self.value, object_hook=self._hook)

    def __init__(self,
            value: Any,
            allow_none: Optional[bool]=None,
            class_info: Any=None,
            min: Optional[int]=None,
            max: Optional[int]=None,
            hook: Optional[FunctionType]=None):
        self._hook = self._object_hook if hook is None else hook
        super(Json, self).__init__(value, allow_none, class_info, min, max)

    def _object_hook(self, obj):
        for (key, value) in obj.items():
            try:
                obj[key] = value.isoformat()
            except:
                pass
        return obj

    def _is_json(self, json_str):
        try:
            json.loads(json_str, object_hook=self._object_hook)
            return True
        except:
            return False

    def conditions(self, value: Any) -> bool:
        return (self._allow_none and value is None) or\
            (
                isinstance(value, self._class_info) and\
                (self._min <= len(value) and len(value) <= self._max) and\
                self._is_json(value)
            )

class Csv(Length):
    CLASS_INFO = str
    LINE_FEED  = '\n'
    DELIMITER  = ','
    QUOTECHAR  = None

    @property
    def list(self):
        return list(self._reader(self.value))

    def __init__(self,
            value: Any,
            allow_none: Optional[bool]=None,
            class_info: Any=None,
            min: Optional[int]=None,
            max: Optional[int]=None,
            line_feed: Optional[str]=None,
            delimiter: Optional[str]=None,
            quotechar: Optional[str]=None):
        self._line_feed = self.LINE_FEED if line_feed is None else line_feed
        self._delimiter = self.DELIMITER if delimiter is None else delimiter
        self._quotechar = self.QUOTECHAR if quotechar is None else quotechar
        super(Csv, self).__init__(value, allow_none, class_info, min, max)

    def _reader(self, csv_str: str) -> csv.reader:
        return csv.reader(
            csv_str.split(self._line_feed),
            delimiter=self._delimiter,
            quotechar=self._quotechar
        )

    def _is_csv(self, csv_str: str) -> bool:
        try:
            self._reader(csv_str)
            return True
        except:
            return False

    def conditions(self, value: Any) -> bool:
        return (self._allow_none and value is None) or\
            (
                isinstance(value, self._class_info) and\
                (self._min <= len(value) and len(value) <= self._max) and\
                self._is_csv(value)
            )