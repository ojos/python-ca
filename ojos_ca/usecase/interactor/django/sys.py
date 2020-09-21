from typing import Any

from django.http.request import HttpRequest

from ojos_ca.domain.value_object.exception import InvalidValueException
from ojos_ca.interface.repo.django import SeqRepo, SysVarRepo
from ojos_ca.usecase.interactor.core import RepoInteractor
from ojos_ca.usecase.interactor.exception import (
    BadRequestException, ConflictException, NotFoundException
)

from .core import RequestInteractor


class SeqRequestInteractor(RepoInteractor, RequestInteractor):
    def __init__(self, repo: SeqRepo, *args, **kwargs):
        super(SeqRequestInteractor, self).__init__(repo, *args, **kwargs)

    def exec(self, request: HttpRequest, seq_id: str=None, *args, **kwargs) -> Any:
        return {'content': {'seq_id': seq_id}}


class GetSeqInteractor(SeqRequestInteractor):
    def exec(self, request: HttpRequest, seq_id: str=None, *args, **kwargs) -> Any:
        if seq_id is None:
            content = [self._repo.serializer.entity_to_dict(seq) for seq in self._repo.find_all()]
        else:
            seq = self._repo.find_by_key(seq_id)
            if seq is None:
                raise NotFoundException(name='seq_id', value=seq_id)
            content = self._repo.serializer.entity_to_dict(seq)

        return {'content': content}

class PostSeqInteractor(SeqRequestInteractor):
    def exec(self, request: HttpRequest, seq_id: str=None, *args, **kwargs) -> Any:
        try:
            seq = self._repo.serializer.dict_to_entity(**self._repo.serializer.json_to_dict(request.body))
        except InvalidValueException as e:
            raise BadRequestException(message=e.message)

        if self._repo.find_by_key(seq.seq_id) is not None:
            raise ConflictException(name='seq_id', value=seq.seq_id)

        seq, _, _ = self._repo.update_or_create(seq)
        content = self._repo.serializer.entity_to_dict(seq)

        return {'content': content}

class PutSeqInteractor(SeqRequestInteractor):
    def exec(self, request: HttpRequest, seq_id: str=None, *args, **kwargs) -> Any:
        seq = self._repo.find_by_key(seq_id)
        if seq is None:
            raise NotFoundException(name='seq_id', value=seq_id)

        try:
            _count = self._repo.serializer.json_to_dict(request.body).get('count', seq.count)
        except InvalidValueException as e:
            raise BadRequestException(message=e.message)

        if seq.count != _count:
            seq.count = _count
            seq, _, _ = self._repo.update_or_create(seq)

        content = self._repo.serializer.entity_to_dict(seq)

        return {'content': content}

class DeleteSeqInteractor(SeqRequestInteractor):
    def exec(self, request: HttpRequest, seq_id: str=None, *args, **kwargs) -> Any:
        seq = self._repo.find_by_key(seq_id)
        if seq is None:
            raise NotFoundException(name='seq_id', value=seq_id)

        self._repo.delete(seq_id)

        return {'message': 'No Content', 'status_code': 204}


class SysVarRequestInteractor(RepoInteractor, RequestInteractor):
    def __init__(self, repo: SysVarRepo, *args, **kwargs):
        super(SysVarRequestInteractor, self).__init__(repo, *args, **kwargs)

    def exec(self, request: HttpRequest, key: str=None, *args, **kwargs) -> Any:
        return {'content': {'key': key}}

class GetSysVarViewInteractor(SysVarRequestInteractor):
    def exec(self, request: HttpRequest, key: str=None, *args, **kwargs) -> Any:
        if key is None:
            content = [self._repo.serializer.entity_to_dict(sysvar) for sysvar in self._repo.find_all()]
        else:
            seq = self._repo.find_by_key(key)
            if seq is None:
                raise NotFoundException(name='key', value=key)
            content = self._repo.serializer.entity_to_dict(seq)

        return {'content': content}

class PostSysVarViewInteractor(SysVarRequestInteractor):
    def exec(self, request: HttpRequest, key: str=None, *args, **kwargs) -> Any:
        try:
            sysvar = self._repo.serializer.dict_to_entity(**self._repo.serializer.json_to_dict(request.body))
        except InvalidValueException as e:
            raise BadRequestException(message=e.message)

        if self._repo.find_by_key(sysvar.key) is not None:
            raise ConflictException(name='key', value=sysvar.key)

        sysvar, _, _ = self._repo.update_or_create(sysvar)
        content = self._repo.serializer.entity_to_dict(sysvar)

        return {'content': content}

class PutSysVarViewInteractor(SysVarRequestInteractor):
    def exec(self, request: HttpRequest, key: str=None, *args, **kwargs) -> Any:
        sysvar = self._repo.find_by_key(key)
        if sysvar is None:
            raise NotFoundException(name='key', value=key)

        _sysvar = self._repo.serializer.json_to_dict(request.body)
        
        try:
            sysvar.raw_data = _sysvar.get('raw_data', sysvar.raw_data)
            sysvar.module = _sysvar.get('module', sysvar.module)
            sysvar.note = _sysvar.get('note', sysvar.note)
        except InvalidValueException as e:
            raise BadRequestException(message=e.message)

        sysvar, _, _ = self._repo.update_or_create(sysvar)
        content = self._repo.serializer.entity_to_dict(sysvar)

        return {'content': content}

class DeleteSysVarViewInteractor(SysVarRequestInteractor):
    def exec(self, request: HttpRequest, key: str=None, *args, **kwargs) -> Any:
        sysvar = self._repo.find_by_key(key)
        if sysvar is None:
            raise NotFoundException(name='key', value=key)

        self._repo.delete(key)

        return {'message': 'No Content', 'status_code': 204}

