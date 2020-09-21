from datetime import date, datetime, time, timezone, MINYEAR, MAXYEAR
from typing import Any, Optional

from ojos.conv.datetime import as_tz, dt_to_int, int_to_dt, LOCAL_ZONE

from ojos_ca.domain.value_object.num import Range


class DatetimeRange(Range):
    CLASS_INFO  = datetime
    MIN         = as_tz(datetime(1970, 1, 1, 0, 0), zone='UTC')
    MAX         = as_tz(datetime(MAXYEAR - 1, 12, 31, 23, 59), zone='UTC')
    MICROSECOND = False
    TIME_ZONE   = LOCAL_ZONE

    @property
    def isoformat(self) -> str:
        return self.value.isoformat()

    @property
    def timestamp(self) -> int:
        return dt_to_int(self.value, self._microsecond)

    def __init__(self,
            value: Any,
            allow_none: Optional[bool]=None,
            class_info: Any=None,
            min: Optional[int]=None,
            max: Optional[int]=None,
            min_equal: Optional[bool]=None,
            max_equal: Optional[bool]=None,
            microsecond: Optional[bool]=None,
            zone: Optional[str]=None):
        self._microsecond = self.MICROSECOND if microsecond is None else microsecond
        self._zone = self.TIME_ZONE if zone is None else zone
        super(DatetimeRange, self).__init__(value, allow_none, class_info, min, max, min_equal, max_equal)

    def __str__(self):
        return self.isoformat

    def __repr__(self):
        return "<{}('{}')>".format(self.__class__.__name__, self.isoformat)

    def pre_set(self, value: Any):
        if value is None:
            return value

        if isinstance(value, datetime):
            value = as_tz(value, zone=self._zone)
        elif isinstance(value, date):
            value = as_tz(datetime.combine(value, time()), zone=self._zone)
        # elif isinstance(value, int):
        #     value = int_to_dt(
        #         value,
        #         microsecond=self._microsecond,
        #         zone=self._zone)
        # elif isinstance(value, str):
        #     value = as_tz(
        #         datetime.fromisoformat(value).astimezone(timezone.utc),
        #         zone=self._zone)

        if value.tzinfo is not None:
            self._min = as_tz(self._min, zone=self._zone)
            self._max = as_tz(self._max, zone=self._zone)
        return value
