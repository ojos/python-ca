from decimal import Decimal
from typing import Any, Optional

from ojos_ca.domain.value_object.core import IsInstance


class Range(IsInstance):
    CLASS_INFO = (int, float)
    MIN        = 0
    MAX        = float('inf')
    MIN_EQUAL  = True
    MAX_EQUAL  = True

    @property
    def string(self) -> str:
        return str(self.value)

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
        super(Range, self).__init__(value, allow_none, class_info)

    def _conditions(self, value: Any) -> bool:
        return super(Range, self)._conditions(value) and (
            (self._min <= value if self._min_equal else self._min < value) and \
            (self._max >= value if self._max_equal else self._max > value)
        )

class DecimalRange(Range):
    CLASS_INFO = Decimal

    def __repr__(self):
        return "<{}({})>".format(self.__class__.__name__, self.value.__repr__)
