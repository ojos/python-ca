from typing import Optional, Union

from ojos_ca.domain.entity.core import Entity

from ojos_ca.domain.value_object.s3 import (
    S3Key, S3ACL, S3ObjectBody,
    S3ObjectContentType, S3ObjectCacheControl, S3ObjectContentEncoding,
    S3SummarySize
)


class S3Object(Entity):

    def __init__(self,
            key: Union[str, bytes],
            content_type: str,
            body: Union[str, bytes, None]=None,
            acl: Optional[str]=None,
            cache_control: Optional[str]=None,
            content_encoding: Optional[str]=None, *args, **kwargs):
        self.key              = key
        self.content_type     = content_type
        self.body             = body
        self.acl              = acl
        self.cache_control    = cache_control
        self.content_encoding = content_encoding

    def __it__(self, other):
        return self.key < other.key

    @property
    def map(self):
        return {'key':              self.key,
                'content_type':     self.content_type,
                'body':             self.body,
                'acl':              self.acl,
                'cache_control':    self.cache_control,
                'content_encoding': self.content_encoding,}

    @property
    def pk(self):
        return 'key'

    @property
    def key(self) -> str:
        return self._key.value

    @key.setter
    def key(self, value: Union[str, bytes]):
        self._key = S3Key(value)

    @property
    def content_type(self) -> str:
        return self._content_type.value

    @content_type.setter
    def content_type(self, value: str):
        self._content_type = S3ObjectContentType(value)

    @property
    def body(self) -> Union[str, bytes, None]:
        return self._body.value

    @body.setter
    def body(self, value: Union[str, bytes, None]):
        self._body = S3ObjectBody(value)

    @property
    def acl(self) -> Optional[str]:
        return self._acl.value

    @acl.setter
    def acl(self, value: Optional[str]):
        self._acl = S3ACL(value)

    @property
    def cache_control(self) -> Optional[str]:
        return self._cache_control.value

    @cache_control.setter
    def cache_control(self, value: Optional[str]):
        self._cache_control = S3ObjectCacheControl(value)

    @property
    def content_encoding(self) -> Optional[str]:
        return self._content_encoding.value

    @content_encoding.setter
    def content_encoding(self, value: Optional[str]):
        self._content_encoding = S3ObjectContentEncoding(value)

class S3Summary(Entity):
    def __init__(self, key: Union[str, bytes],
                       size: int, *args, **kwargs):
        self.key  = key
        self.size = size

    def __it__(self, other):
        return self.size < other.size

    @property
    def pk(self):
        return 'key'

    @property
    def map(self):
        return {'key':  self.key,
                'size': self.size,}

    @property
    def key(self) -> str:
        return self._key.value

    @key.setter
    def key(self, value: Union[str, bytes]):
        self._key = S3Key(value)

    @property
    def size(self) -> int:
        return self._size.value

    @size.setter
    def size(self, value: int):
        self._size = S3SummarySize(value)

