from django.db import models

from ojos_ca.domain.value_object.sys import (
    SeqCount, SeqId,
    SysVarKey, SysVarModule, SysVarNote, SysVarRawData
)

from .core import BaseModel, ValidationWrapper


class SeqModel(BaseModel):
    seq_id = models.CharField(
        primary_key=True,
        max_length=SeqId.MAX,
        validators=[ValidationWrapper(SeqId).validate],
        verbose_name='シーケンスID'
    )
    count      = models.PositiveIntegerField(
        validators=[ValidationWrapper(SeqCount).validate],
        verbose_name='カウント'
    )

    def __str__(self):
        return self.seq_id

    class Meta(BaseModel.Meta):
        # managed                            = False
        db_table                           = 'app_sequence'
        verbose_name = verbose_name_plural = ' シーケンス'

class SysVarModel(BaseModel):
    key      = models.CharField(
        primary_key=True,
        max_length=SysVarKey.MAX,
        validators=[ValidationWrapper(SysVarKey).validate],
        verbose_name='変数名'
    )
    raw_data = models.TextField(
        max_length=SysVarRawData.MAX,
        blank=True,
        null=False,
        validators=[ValidationWrapper(SysVarRawData).validate],
        verbose_name='変換前の値'
    )
    module   = models.CharField(
        max_length=SysVarModule.MAX,
        default=SysVarModule.DEFAULT_VALUE,
        validators=[ValidationWrapper(SysVarModule).validate],
        verbose_name='出力時の変換型'
    )
    note     = models.TextField(
        max_length=SysVarNote.MAX,
        blank=True,
        null=False,
        default=SysVarNote.DEFAULT_VALUE,
        validators=[ValidationWrapper(SysVarNote).validate],
        verbose_name='備考'
    )

    def __str__(self):
        return self.key

    class Meta(BaseModel.Meta):
        # managed                            = False
        db_table                           = 'app_variable'
        verbose_name = verbose_name_plural = 'システム変数'
