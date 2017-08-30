# -*- coding: utf-8 -*-
# Owner: Bulat <bulat.kurbangaliev@cinarra.com>
import logging
import math

from marshmallow import ValidationError

logger = logging.getLogger(__name__)


def get_string_validator(max_length=None, choices=None):
    def validator(s):
        if not isinstance(s, str):
            raise ValidationError('Given string is not a type string')
        if choices and s not in choices:
            raise ValidationError('Given string not in {}'.format(choices))
        if max_length and len(s) >= max_length:
            raise ValidationError('Given string length more than {}'.format(max_length))
        return s

    return validator


def get_int_validator(rank=None, _range=None):
    def validator(i):
        try:
            i = int(i)
        except ValueError:
            raise ValidationError('Can not parse int from string')
        except TypeError as e:
            raise ValidationError(e.message)
        if rank and math.log10(i) + 1 > rank:
            raise ValidationError('Given number with rank more than {}'.format(rank))
        if _range and i not in range(*_range):
            raise ValidationError('Given number is not in range {}'.format(_range))
        if not isinstance(i, int):
            raise ValidationError('Given number is not a type number')
        return i

    return validator
