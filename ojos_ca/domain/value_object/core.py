import sys
from typing import Any, Optional

from ojos_ca.domain.value_object.exception import InvalidValueException


class ValueObject(object):
    EXCEPTION  = InvalidValueException
    ALLOW_NONE = False

    @property
    def value(self) -> Any:
        return self.__value

    @value.setter
    def value(self, value: Any):
        try:
            value = self.pre_set(value)
        except:
            raise self.EXCEPTION(
                name=self.__class__.__name__,
                value=value)

        if self.conditions(value):
            try:
                self.__value = self.post_set(value)
            except:
                raise self.EXCEPTION(
                    name=self.__class__.__name__,
                    value=value)
        else:
            raise self.EXCEPTION(
                name=self.__class__.__name__,
                value=value)

    def __init__(self, 
            value: Any,
            allow_none: Optional[bool]=None):
        self._allow_none = self.ALLOW_NONE if allow_none is None else allow_none
        self.value = value

    def __str__(self):
        return '{}'.format(self.value)

    def __repr__(self):
        return '<{}({})>'.format(self.__class__.__name__, self.value)

    def _is_allow_none(self, allow_none: Any) -> bool:
        return self._allow_none and allow_none is None

    def _conditions(self, value: Any) -> bool:
        return True

    def pre_set(self, value: Any) -> Any:
        return value

    def post_set(self, value: Any) -> Any:
        return value

    def conditions(self, value: Any) -> bool:
        return self._is_allow_none(value) or self._conditions(value)

class IsInstance(ValueObject):
    CLASS_INFO = (int, float)

    def __init__(self, 
            value: Any,
            allow_none: Optional[bool]=None,
            class_info: Any=None):
        self._class_info = self.CLASS_INFO if class_info is None else class_info
        super(IsInstance, self).__init__(value, allow_none)

    def _conditions(self, value: Any) -> bool:
        return isinstance(value, self._class_info)

class Choice(ValueObject):
    CHOICES    = []

    def __init__(self,
            value: Any,
            allow_none: Optional[bool]=None,
            choices: Optional[list]=None):
        self._choices = self.CHOICES if choices is None else choices
        super(Choice, self).__init__(value, allow_none)

    def _conditions(self, value: Any) -> bool:
        return value in self._choices

class Length(IsInstance):
    CLASS_INFO = (str, bytes)
    MIN        = 0
    MAX        = sys.maxsize
    MIN_EQUAL  = True
    MAX_EQUAL  = True

    @property
    def length(self) -> Optional[int]:
        return len(self.value)

    def __init__(self, 
            value: Any,
            allow_none: Optional[bool]=None,
            class_info: Any=None,
            min: Optional[int]=None,
            max: Optional[int]=None,
            min_equal: Optional[bool]=None,
            max_equal: Optional[bool]=None):
        self._min = self.MIN if min is None else min
        self._max = self.MAX if max is None else max
        self._min_equal = self.MIN_EQUAL if min_equal is None else min_equal
        self._max_equal = self.MAX_EQUAL if max_equal is None else max_equal
        super(Length, self).__init__(value, allow_none, class_info)

    def _conditions(self, value: Any) -> bool:
        return super(Length, self)._conditions(value) and (
            (self._min <= len(value) if self._min_equal else self._min < len(value)) and \
            (self._max >= len(value) if self._max_equal else self._max > len(value))
        )


class Nest(ValueObject):
    CLASS_INFO  = IsInstance
    ALLOW_EMPTY = False

    def __init__(self, 
            value: Any,
            allow_none: Optional[bool]=None,
            class_info: Any=None,
            allow_empty: Optional[bool]=None):
        self._class_info = self.CLASS_INFO if class_info is None else class_info
        self._allow_empty = self.ALLOW_EMPTY if allow_empty is None else allow_empty
        super(Nest, self).__init__(value, allow_none)

    def _conditions(self, value: Any) -> bool:
        try:
            self._class_info(value)
            return True
        except:
            return False

    def _down(self, value: Any) -> bool:
        if not self._allow_empty and len(value) == 0:
            return False

        for nest_value in value:
            if not self._conditions(nest_value):
                return False
        return True

    def conditions(self, value: Any) -> bool:
        return super(Nest, self).conditions(value) or self._down(value)