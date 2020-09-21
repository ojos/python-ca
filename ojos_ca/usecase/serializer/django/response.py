import sys
from typing import Optional, Union, Tuple

from logging import basicConfig, getLogger, INFO

from django.http.response import HttpResponse
from django.utils import timezone

from ojos.conv.datetime import as_tz

from ..core import JsonSerializer


basicConfig()
logger = getLogger(__name__)
logger.setLevel(INFO)


class HttpResponseSerializer(object):
    @classmethod
    def to_response(cls, 
            content: Union[str, bytes]='',
            headers: dict={},
            content_type: str='text/html; charset=utf-8',
            status_code: int=200) -> HttpResponse:
        response = HttpResponse(
            content=content,
            status=status_code,
            content_type=content_type,
        )
        for key, val in headers.items():
            response[key] = val

        return response

    @classmethod
    def get_error_context(cls, e: Exception) -> Tuple[str, int]:
        logger.exception('EXCEPTION: {}'.format(e))
        if hasattr(e, 'message'):
            message = e.message
        else:
            message = '{}'.format(e.with_traceback(sys.exc_info()[2]))
        status_code = e.status_code if hasattr(e, 'status_code') else 500
        return message, status_code

    @classmethod
    def error_to_response(cls, e: Exception) -> HttpResponse:
        message, status_code = cls.get_error_context(e)
        return cls.to_response(message, status_code=status_code)



class JsonApiResponseSerializer(HttpResponseSerializer):
    @classmethod
    def to_response(cls, 
            content: Optional[dict]=None,
            headers: dict={},
            status_code: int=200,
            message: str='OK',
            ensure_ascii: bool=False,
            indent: Optional[int]=None,
            dt_dist: Union[str, int]=str) -> HttpResponse:
        body = {'code':       status_code,
                'message':    message,
                'servertime': as_tz(timezone.now())}

        if content is not None:
            body['content'] = content

        response = HttpResponseSerializer.to_response(
            JsonSerializer.dict_to_json(body, ensure_ascii, indent, dt_dist),
            headers={
                'Cache-Control': 'no-cache, max-age=0'
            },
            content_type='application/json; charset=utf-8',
            status_code=status_code
        )

        return response

    @classmethod
    def error_to_response(cls, e: Exception) -> HttpResponse:
        message, status_code = cls.get_error_context(e)
        return cls.to_response(message=message, status_code=status_code)