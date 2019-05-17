"""Configuration via environment"""
import json
import re
from datetime import date, datetime, time, timedelta
from os import environ

__version__ = '0.1.0'
__all__ = ['populate_from_env', 'register_type_parser']


def populate_from_env(obj, prefix='', env=None):
    """Populate values in obj from environment. obj should have
    __annotations__ attribute.

    >>> from datetime import timedelta
    >>> from viaenv import populate_from_env
    >>> class config:
    ...     port: int = 8080
    ...     log_file: str = '/var/log/server.log'
    ...     timeout: timedelta = timedelta(milliseconds=100)
    ...
    >>> populate_from_env(
    ...     config, prefix='SRV',
    ...     # If you don't pass env, populate_from_env will use os.environ
    ...     env={'SRV_PORT': '9000', 'SRV_TIMEOUT': '300ms'})
    >>> config.port
    9000
    >>> config.timeout == timedelta(milliseconds=300)
    True
    """
    if not hasattr(obj, '__annotations__'):
        raise ValueError(f'no type annotation in {obj!r} of type')

    env = environ if env is None else env
    cfg = {}  # We first populate cfg, and only if all succeed update obj

    if prefix:
        prefix = prefix + '_'

    for name, typ in obj.__annotations__.items():
        env_name = prefix + name.upper()
        value = env.get(env_name)
        if value is None:
            continue

        parser = find_parser(typ)
        cfg[name] = parser(value)

    for name, value in cfg.items():
        setattr(obj, name, value)


_type_parsers = {}


def register_type_parser(typ, parser):
    """Register a parser for type "typ", "parser" should be a function that
    gets one string value and returned parsed type.
    """
    # TODO: warn on duplicates
    _type_parsers[typ] = parser


def find_parser(typ):
    for cls, func in _type_parsers.items():
        if issubclass(typ, cls):
            return func
    return typ


def type_parser(typ):
    def wrapper(func):
        register_type_parser(typ, func)
        return func
    return wrapper


@type_parser(int)
def parse_int(value):
    return int(value, 0)  # Allow 10, 0x10, 0o10, 0b10

# TODO: Allow adding/chaning formats
@type_parser(datetime)
def parse_datetime(value):
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')


@type_parser(time)
def parse_time(value):
    return time.fromisoformat(value)


@type_parser(date)
def parse_date(value):
    return date.fromisoformat(value)


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
