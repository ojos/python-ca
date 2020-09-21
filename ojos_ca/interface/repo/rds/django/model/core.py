import json
from datetime import datetime
from typing import Any

from django.db import models
from django.core.exceptions import (
    ImproperlyConfigured, ValidationError
)
from django.utils.translation import gettext_lazy as _

from ojos_ca.domain.value_object.core import ValueObject
from ojos_ca.domain.value_object.exception import InvalidValueException


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name='作成日時',
        auto_now_add=True,
        db_index=True
    )
    updated_at = models.DateTimeField(
        verbose_name='更新日時',
        auto_now=True
    )

    def __repr__(self):
        return self.__str__()

    class Meta:
        abstract      = True
        app_label     = 'app'
        get_latest_by = 'created_at'
        ordering      = ['-created_at']

class NullCharField(models.CharField):
    """
    Subclass of the CharField that allows
    empty strings to be stored as NULL in database
    """
    description = _("CharField that stores '' as None and returns None as ''")

    def __init__(self, *args, **kwargs):
        if not kwargs.get('null', True) or not kwargs.get('blank', True):
            raise ImproperlyConfigured(
                'NullCharField implies null==blank==True')
        kwargs['null'] = kwargs['blank'] = True
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        val = super().to_python(value)
        return '' if val is None else val

    def get_prep_value(self, value):
        prep_value = super().get_prep_value(value)
        return None if prep_value == '' else prep_value

    def deconstruct(self):
        """
        For migration purposes
        """
        name, path, args, kwargs = super().deconstruct()
        del kwargs['null']
        del kwargs['blank']
        return name, path, args, kwargs


class ValidationWrapper(object):
    def __init__(self, vo: ValueObject):
        self._vo = vo

    def validate(self, value: Any):
        try:
            self._vo(value)
        except InvalidValueException as e:
            raise ValidationError(
                _('Enter a valid value: %(value)s')
            )
