import numpy as np
from io import BytesIO
from PIL import Image
from PIL.ImageFile import ImageFile
from typing import Any, Optional

from ojos_ca.domain.value_object.core import Image as _Image


class PILImage(_Image):
    @property
    def image(self) -> Image:
        return Image.open(BytesIO(self.value))

    @property
    def ndarray(self) -> np.ndarray:
        ndarray = np.array(self.image)
        if ndarray.ndim == 2:
            pass
        elif ndarray.shape[2] == 3:
            ndarray = ndarray[:, :, ::-1]
        elif ndarray.shape[2] == 4:
            ndarray = ndarray[:, :, [2, 1, 0, 3]]
        return ndarray

    @property
    def file_format(self) -> str:
        if self._file_format is None:
            self._file_format = self.image.format
        return self._file_format

    def __init__(self,
        value: Any,
        allow_none: Optional[bool]=None,
        class_info: Any=None,
        file_format: Optional[str]=None,):
        self._file_format = file_format
        super(PILImage, self).__init__(value, allow_none, class_info)

    def pre_set(self, value: Any):
        if value is None:
            return value

        if isinstance(value, np.ndarray):
            if value.ndim == 2:
                pass
            elif value.shape[2] == 3:
                value = value[:, :, ::-1]
            elif value.shape[2] == 4:
                value = value[:, :, [2, 1, 0, 3]]
            value = Image.fromarray(value)

        if isinstance(value, (ImageFile, Image.Image)):
            if self._file_format is None:
                self._file_format = value.format
            bio = BytesIO()
            value.save(bio, format=self._file_format)
            value = bio.getvalue()

        return super(PILImage, self).pre_set(value)

