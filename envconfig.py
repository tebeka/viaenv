"""Configuration via environment"""
import json
import re
from datetime import date, datetime, time, timedelta
from os import environ

_type_parsers = {}


def add_type_parser(typ, parser):
    # TODO: warn on duplicates
    _type_parsers[typ] = parser


def from_env(obj, prefix='', env=None):
    if not hasattr(obj, '__annotations__'):
        raise ValueError(f'no type annotation in {obj!r} of type')

    env = environ if env is None else env

    if prefix:
        prefix = prefix + '_'

    for name, typ in obj.__annotations__.items():
        env_name = prefix + name.upper()
        value = env.get(env_name)
        if value is None:
            continue

        parser = find_parser(typ)
        value = parser(value)
        setattr(obj, name, value)


def find_parser(typ):
    for pt, func in _type_parsers.items():
        if isinstance(typ, pt):
            return func
    return typ


def type_parser(typ):
    def wrapper(func):
        add_type_parser(typ, func)
        return func
    return wrapper


# TODO: Allow adding/chaning formats
_datetime_fmt = '%Y-%m-%dT%H%M:%S'


@type_parser(datetime)
def parse_datetime(value):
    return datetime.strptime(value, _datetime_fmt)


_time_fmt = '%H:%M'


@type_parser(time)
def parse_time(value):
    return time.strptime(value, _time_fmt)


_date_fmt = '%Y-%m-%d'


@type_parser(date)
def parse_date(value):
    return date.strptime(value, _date_fmt)


_second = int(1e6)
_time_units = {
    'us': 1,
    'ms': 1_000,
    's': _second,
    'm': 60 * _second,
    'h': 60 * 60 * _second,
    'd': 24 * 60 * 60 * _second,
}


@type_parser(timedelta)
def parse_timedelta(value):
    us = 0
    # 10m30s
    for amount, unit in re.findall(r'([0-9]+)([a-zA-Z]+)', value):
        n = _time_units.get(unit.lower())
        if n is None:
            raise ValueError(f'unknown time unit {unit!r} in {value!r}')
        us += n * int(amount)
    return timedelta(microseconds=us)


@type_parser(list)
def parse_list(value):
    lval = json.loads(value)
    if not isinstance(lval, list):
        raise TypeError(f'{value!r} is not a list')
    return lval


@type_parser(dict)
def parse_dict(value):
    dval = json.loads(value)
    if not isinstance(dval, dict):
        raise TypeError(f'{value!r} is not a dict')
    return dval
