# py-expiring-dict
Python dict with TTL support for auto-expiring caches


# Install
```bash
pip install expiring-dict
```

# Usage
## Class Level TTL
```python
from time import sleep
from expiring_dict import ExpiringDict

cache = ExpiringDict(1)  # Keys will exist for 1 second

cache["abc123"] = "some value"
assert "abc123" in cache
sleep(1)
assert "abc123" not in cache
```

## Key Level TTL
```python
from time import sleep
from expiring_dict import ExpiringDict

cache = ExpiringDict()  # No TTL set, keys set via [] will not expire

cache["abc"] = "persistent"
cache.ttl("123", "expired", 1)  # This will expire after 1 second
assert "abc" in cache
assert "123" in cache
sleep(1)
assert "abc" in cache
assert "123" not in cache
```
