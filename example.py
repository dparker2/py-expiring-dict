from time import sleep
from expiring_dict import ExpiringDict

cache = ExpiringDict()  # No TTL set, keys set via [] will not expire

cache["abc"] = "persistent"
cache.ttl("123", "expires", 1)  # This will expire after 1 second
print("abc" in cache)
print("123" in cache)
sleep(1.1)
print("abc" in cache)
print("123" not in cache)

cache2 = ExpiringDict(1)

cache2["abc"] = "expires"
cache2["123"] = "also expires"
print("abc" in cache2)
print("123" in cache2)
sleep(1.1)
print("abc" not in cache2)
print("123" not in cache2)
