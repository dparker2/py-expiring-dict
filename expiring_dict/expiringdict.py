try:
    from collections.abc import MutableMapping
except ImportError:  # Will allow usage with virtually any python 3 version
    from collections import MutableMapping

from threading import Thread, Lock
from sortedcontainers import SortedKeyList
from time import time, sleep


class ExpiringDict(MutableMapping):
    def __init__(self, ttl=None, interval=0.100, *args, **kwargs):
        """
        Create an ExpiringDict class, optionally passing in a time-to-live
        number in seconds that will act globally as an expiration time for keys.

        If omitted, the dict will work like a normal dict by default, expiring
        only keys explicity set via the `.ttl` method.
        """
        now = time()
        self.__store = dict(*args, **kwargs)
        self.__keys = SortedKeyList(key=lambda x: x[0])
        self.__time_last_set = {k: now for k in self.__store}
        self.__ttl = ttl
        self.__lock = Lock()
        self.__interval = interval

        Thread(target=self.__worker, daemon=True).start()

    def flush(self):
        now = time()
        del_index = 0

        with self.__lock:
            for index, (timestamp, set_at, key) in enumerate(self.__keys):
                if timestamp > now:  # Rest of the timestamps in future
                    break

                del_index = index + 1

                if self.__time_last_set[key] > set_at:
                    continue  # This key was set again at some point, don't delete from store

                try:
                    del self.__store[key]
                except KeyError:
                    pass  # Don't care if it was deleted early
                try:
                    del self.__time_last_set[key]
                except KeyError:
                    pass
            del self.__keys[0:del_index]

    def __worker(self):
        while True:
            self.flush()
            sleep(self.__interval)

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
        now = time()

        with self.__lock:
            self.__keys.add((now + ttl, now, key))
            self.__store[key] = value
            self.__time_last_set[key] = now

    def __delitem__(self, key):
        del self.__store[key]

    def __getitem__(self, key):
        return self.__store[key]

    def __iter__(self):
        return iter(self.__store)

    def __len__(self):
        return len(self.__store)
