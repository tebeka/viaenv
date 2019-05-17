from datetime import timedelta, datetime, date, time

import pytest

import viaenv

parse_cases = [
    ('hello', 'hello'),
    ('8080', 8080),
    ('1.3', 1.3),
    ('10s', timedelta(seconds=10)),
    ('[1, 2, 3]', [1, 2, 3]),
    ('{"x": 1, "y": 2}', {'x': 1, 'y': 2}),
    ('2019-05-18T13:43:12', datetime(2019, 5, 18, 13, 43, 12)),
    ('2019-05-18', date(2019, 5, 18)),
    ('13:43:12', time(13, 43, 12)),
]


@pytest.mark.parametrize('env_val, val', parse_cases)
def test_parsers(env_val, val):
    func = viaenv.find_parser(type(val))
    assert func, f'no parser for {val!r} of type {type(val)}'
    out = func(env_val)
    assert val == out, 'value mismatch'
