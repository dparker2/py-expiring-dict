from time import sleep
from expiring_dict import ExpiringDict

cache = ExpiringDict()  # No TTL set, keys set via [] will not expire

cache["abc"] = "persistent"
cache.ttl("123", "expired", 1)  # This will expire after 1 second
print("abc" in cache)
print("123" in cache)
sleep(1)
print("abc" in cache)
print("123" not in cache)
