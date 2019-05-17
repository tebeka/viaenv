# viaenv - Configuration via Environment for Python

`viaenv` uses [variable annotation](https://www.python.org/dev/peps/pep-0526/)
to populate values from environment variables.

## Example

```python
from datetime import timedelta
from viaenv import populate_from_env


class config:
    port: int = 8080
    log_file: str = '/var/log/server.log'
    timeout: timedelta = timedelta(milliseconds=100)


populate_from_env(
    config, prefix='srv',
    # If you don't pass env, populate_from_env will use os.environ
    env={'SRV_PORT': '9000', 'SRV_TIMEOUT': '300ms'})

print(config.port)  # 9000
print(cfg.timeout == timedelta(milliseconds=300)  # True
```

## Supported Types

- `date`: `2019-05-18`
- `datetime`: `2019-05-18T13:43:12`
- `dict`: `{"x": 1, "y": 2}` (JSON format)
- `float`: `1.3`, `1e7`
- `int`: `12`, `0x12`, `0o12`, `0b12`
- `list`: `[1, 2, 3]` (JSON format)
- `str`: Anything goes
- `time`: `13:43:12`
- `timedelta`: `10us`, `20ms`, `30s`, `17m`, `2h`, `7d`, `1h20m`

You can add your types by calling 
