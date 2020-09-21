import base64
import re
from typing import Any

from ojos_ca.domain.value_object.core import IsInstance


class Binary(IsInstance):
    CLASS_INFO = bytes

    @property
    def base64(self) -> str:
        return base64.b64encode(self.value).decode()

    def pre_set(self, value: Any):
        if value is None:
            return value

        if isinstance(value, str):
            return base64.b64decode(value.encode())
        else:
            return value

class BinaryFile(Binary):
    @property
    def mime_type(self):
        return self._mime_type

    @property
    def extension(self):
        return self._extension

class Image(BinaryFile):
    def _is_jpg(self, value: bytes) -> bool:
        if bool(re.match(br"^\xff\xd8", value[:2])):
            self._mime_type = 'image/jpeg'
            self._extension = 'jpg'
            return True
        return False

    def _is_png(self, value: bytes) -> bool:
        if bool(re.match(br"^\x89\x50\x4e\x47", value[:4])):
            self._mime_type = 'image/png'
            self._extension = 'png'
            return True
        return False

    def _is_gif(self, value: bytes) -> bool:
        if bool(re.match(br"^\x47\x49\x46\x38", value[:4])):
            self._mime_type = 'image/gif'
            self._extension = 'gif'
            return True
        return False

    def _is_bmp(self, value: bytes) -> bool:
        if bool(re.match(br"^\x42\x4d", value[:2])):
            self._mime_type = 'image/bmp'
            self._extension = 'bmp'
            return True
        return False

    def _is_tiff(self, value: bytes) -> bool:
        if bool(re.match(br"^\x00\x2a", value[:2])):
            self._mime_type = 'image/tiff'
            self._extension = 'tiff'
            return True
        return False

    def conditions(self, value: Any) -> bool:
        return self._is_jpg(value) or self._is_png(value) or self._is_gif(value) or\
            self._is_bmp(value) or self._is_tiff(value)

class Video(BinaryFile):
    def _is_avi(self, value: bytes) -> bool:
        if bool(re.match(br"^\x52\x49\x46\x46", value[:4])):
            self._mime_type = 'video/x-msvideo'
            self._extension = 'avi'
            return True
        return False

    def _is_wmv(self, value: bytes) -> bool:
        if bool(re.match(br"^\x30\x26\xB2\x75\x8E\x66\xCF\x11\xA6\xD9\x00\xAA\x00\x62\xCE\x6C", value[:16])):
            self._mime_type = 'video/x-ms-wmv'
            self._extension = 'wmv'
            return True
        return False

    def _is_mov(self, value: bytes) -> bool:
        if bool(re.match(br"^\x00\x00\x00\x14\x66\x74\x79\x70\x71\x74\x20\x20\x00\x00\x00\x00\x71\x74\x20\x20\x00\x00\x00\x08\x77\x69\x64\x65", value[:28])):
            self._mime_type = 'video/quicktime'
            self._extension = 'mov'
            return True
        return False

    def _is_mp4(self, value: bytes) -> bool:
        if bool(re.match(br"^\x00\x00\x00\x20\x66\x74\x79\x70\x69\x73\x6F\x6D\x00\x00\x02\x00", value[:16])):
            self._mime_type = 'video/mp4'
            self._extension = 'mp4'
            return True
        return False

    def _is_webm(self, value: bytes) -> bool:
        if bool(re.match(br"^\x1a\x45\xdf\xa3", value[:4])):
            self._mime_type = 'video/webm'
            self._extension = 'webm'
            return True
        return False

    def conditions(self, value: Any) -> bool:
        return self._is_avi(value) or self._is_wmv(value) or self._is_mov(value) or\
            self._is_mp4(value) or self._is_webm(value)

# class Audio(BinaryFile):
#     def _is_midi(self, value: bytes) -> bool:
#         if bool(re.match(br"^\x52\x49\x46\x46", value[:4])):
#             self._mime_type = 'audio/midi'
#             self._extension = 'midi'
#             return True
#         return False

#     def _is_wav(self, value: bytes) -> bool:
#         if bool(re.match(br"^\x1a\x45\xdf\xa3", value[:4])):
#             self._mime_type = 'audio/x-wav'
#             self._extension = 'wav'
#             return True
#         return False

#     def _is_mp3(self, value: bytes) -> bool:
#         if bool(re.match(br"^\x30\x26\xB2\x75\x8E\x66\xCF\x11\xA6\xD9\x00\xAA\x00\x62\xCE\x6C", value[:16])):
#             self._mime_type = 'audio/mpeg'
#             self._extension = 'mp3'
#             return True
#         return False

#     def _is_mp4(self, value: bytes) -> bool:
#         if bool(re.match(br"^\x00\x00\x00\x20\x66\x74\x79\x70\x69\x73\x6F\x6D\x00\x00\x02\x00", value[:16])):
#             self._mime_type = 'audio/mp4'
#             self._extension = 'mp4'
#             return True
#         return False

#     def _is_aiff(self, value: bytes) -> bool:
#         if bool(re.match(br"^\x00\x00\x00\x14\x66\x74\x79\x70\x71\x74\x20\x20\x00\x00\x00\x00\x71\x74\x20\x20\x00\x00\x00\x08\x77\x69\x64\x65", value[:28])):
#             self._mime_type = 'audio/x-aiff'
#             self._extension = 'aiff'
#             return True
#         return False

#     def conditions(self, value: Any) -> bool:
#         return self._is_midi(value) or self._is_wav(value) or self._is_mp3(value) or\
#             self._is_mp4(value) or self._is_aiff(value)
