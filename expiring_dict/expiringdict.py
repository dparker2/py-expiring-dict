from collections.abc import MutableMapping
from threading import Timer


class ExpiringDict(MutableMapping):
    def __init__(self, ttl=None):
        """
        Create an ExpiringDict class, optionally passing in a time-to-live
        number in seconds that will act globally as an expiration time for keys.

        If omitted, the dict will work like a normal dict by default, expiring
        only keys explicity set via the `.ttl` method.
        """
        self.__store = dict()
        self.__expirations = dict()
        self.__ttl = ttl

    def __delitem__(self, key):
        """
        Delete `key` from the dict.
        Raises `KeyError` if key does not exist.
        """
        try:
            del self.__store[key]
        except KeyError:
            raise KeyError
        try:
            self.__expirations[key].cancel()
            del self.__expirations[key]
        except KeyError:
            pass

    def __getitem__(self, key):
        """
        Return value of `key` in dict.
        Raises `KeyError` if key does not exist.
        """
        try:
            return self.__store[key]
        except KeyError:
            raise KeyError

    def get(self, key, default=None):
        """
        Return value of `key` in dict, or default value which defaults to `None`.
        """
        return self.__store.get(key, default)

    def __iter__(self):
        """
        Return iterator of dict.
        """
        return iter(self.__store)

    def __len__(self):
        """
        Return length of dict.
        """
        return len(self.__store)

    def keys(self):
        """
        Return dict keys.
        """
        return self.__store.keys()

    def values(self):
        """
        Return dict values.
        """
        return self.__store.values()

    def items(self):
        """
        Return dict items.
        """
        return self.__store.items()

    def __setitem__(self, key, value):
        """
        Set `value` of `key` in dict. `key` will be automatically
        deleted if the `ttl` option was provided for this object.
        """
        if self.__ttl:
            self.__set_with_expire(key, value, self.__ttl)
        else:
            self.__store[key] = value

    def ttl(self, key, value, ttl):
        """
        Set `value` of `key` in dict to expire after `ttl` seconds.
        Overrides object level `ttl` setting.
        """
        self.__set_with_expire(key, value, ttl)

    def __set_with_expire(self, key, value, ttl):
        def expire():
            try:
                del self[key]
            except KeyError:
                pass

        timer = Timer(ttl, expire)
        timer.start()
        self.__expirations[key] = timer

        self.__store[key] = value
