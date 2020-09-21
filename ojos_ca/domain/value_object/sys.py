from typing import Any, Optional
import sys

from ojos_ca.domain.value_object.core import Length
from ojos_ca.domain.value_object.num import Range


class SeqId(Length):
    MIN       = 1
    MAX       = 64
    MIN_EQUAL = True
    MAX_EQUAL = True

class SeqCount(Range):
    CLASS_INFO = int
    MIN        = 0
    MAX        = sys.maxsize
    MIN_EQUAL  = True
    MAX_EQUAL  = True

class SysVarKey(Length):
    MIN       = 0
    MAX       = 64
    MIN_EQUAL = False
    MAX_EQUAL = True

class SysVarRawData(Length):
    MIN       = 0
    MAX       = 2 ** 32
    MIN_EQUAL = False
    MAX_EQUAL = True

class SysVarModule(Length):
    MIN           = 0
    MAX           = 128
    MIN_EQUAL     = False
    MAX_EQUAL     = True
    DEFAULT_VALUE = 'str'

    def __init__(self, 
            value: Any=None,
            allow_none: Optional[bool]=None,
            class_info: Any=None,
            min: Optional[int]=None,
            max: Optional[int]=None,
            min_equal: Optional[bool]=None,
            max_equal: Optional[bool]=None):
        value = self.DEFAULT_VALUE if value is None else value
        super(SysVarModule, self).__init__(value, allow_none, class_info, min, max, min_equal, max_equal)

class SysVarNote(Length):
    MIN           = 0
    MAX           = 2 ** 10
    MIN_EQUAL     = True
    MAX_EQUAL     = True
    DEFAULT_VALUE = ''

    def __init__(self, 
            value: Any=None,
            allow_none: Optional[bool]=None,
            class_info: Any=None,
            min: Optional[int]=None,
            max: Optional[int]=None,
            min_equal: Optional[bool]=None,
            max_equal: Optional[bool]=None):
        value = self.DEFAULT_VALUE if value is None else value
        super(SysVarNote, self).__init__(value, allow_none, class_info, min, max, min_equal, max_equal)
